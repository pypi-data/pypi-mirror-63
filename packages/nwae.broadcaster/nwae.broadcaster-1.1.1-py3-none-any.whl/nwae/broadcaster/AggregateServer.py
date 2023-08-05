# -*- coding: utf-8 -*-

import flask
import nwae.broadcaster.config.Config as cf
from nwae.utils.Log import Log
from inspect import getframeinfo, currentframe
from nwae.broadcaster.Authenticate import Authenticate
from nwae.utils.ObjectPersistence import ObjectPersistence
import os
import json
from nwae.broadcaster.subscriber.SubscriberSharedSecret import SubscriberSharedSecret


#
# Push & Pull Feed
# This API allows all feed processes to send feed to one place.
# It also allows retrieval (cached for some time)
#
app = flask.Flask(__name__)


#
# Aggregates any feed, and puts them to queue, no processing on data.
# We don't run in multithread using gunicorn, as the API call should be
# very fast, as there is no processing involved, just forwarding.
#
class AggregateServer:

    JSON_ENCODING = 'utf-8'

    def __init__(
            self,
            # Queue to write feed to
            feed_queue,
            # Config object
            config
    ):
        self.feed_queue = feed_queue
        self.config = config

        # For gunicorn to access, and will never change without a restart
        self.port = int(self.config.get_config(param=cf.Config.PARAM_PORT_AGGREGATOR))
        self.feed_cache_folder = self.config.get_config(param=cf.Config.PARAM_FEED_CACHE_FOLDER)
        if not os.path.exists(self.feed_cache_folder):
            raise Exception(
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Feed cache folder "' + str(self.feed_cache_folder)
                + '" does not exist!'
            )
        self.feed_id_key = self.config.get_config(param=cf.Config.PARAM_FEED_ID_KEY)

        self.secret_subscriber_password = SubscriberSharedSecret.init_singleton_config()

        # Flask app
        self.app_feed_aggregator = app
        self.app_feed_aggregator.config['DEBUG'] = False

        self.__init_rest_urls()
        return

    def __init_rest_urls(self):
        @self.app_feed_aggregator.route('/cagg', methods=['POST','GET'])
        def feed_aggregator_push():
            request_json = self.get_request_json(method=flask.request.method)

            mode = 'push'

            if 'mode' in request_json.keys():
                mode = request_json['mode']

            key_subscriber_id = 'user'
            if mode == 'push':
                key_subscriber_id = 'provider'

            subscriber_id = None
            auth = None
            if 'auth' in request_json.keys():
                subscriber_id = request_json[key_subscriber_id]
                auth = request_json['auth']

            res_auth = self.authenticate_connection(
                subscriber_id = subscriber_id,
                auth = auth
            )
            if not res_auth:
                Log.warning(
                    str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                    + ': Subscriber "' + str(subscriber_id) + '" FAILED AUTHENTICATION'
                )
                if mode == 'pull':
                    return 'bad x'
                # TODO For now let all who fail authentication also pass in push mode
            else:
                Log.info(
                    str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                    + ': Subscriber "' + str(subscriber_id) + '" PASSED AUTHENTICATION'
                )

            if mode == 'pull':
                return self.process_feed_pull(request_json=request_json)
            else:
                return self.process_feed_push(request_json=request_json)

        @self.app_feed_aggregator.errorhandler(404)
        def page_not_found(e):
            Log.critical(str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                            + 'Resource [' + str(flask.request.url) + '] is not valid!')
            return "<h1>404</h1><p>The resource could not be found.</p>", 404

    def authenticate_connection(
            self,
            subscriber_id,
            auth
    ):
        shared_secret = self.secret_subscriber_password.get_config(param=subscriber_id)
        if shared_secret is None:
            Log.error(
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Subscriber id "' + str(subscriber_id) + '" not in secret file.'
            )

        authenticator_obj = Authenticate(
            shared_secret  = shared_secret,
            challenge      = None,
            test_challenge = str(auth)
        )
        return authenticator_obj.verify_totp_otp()

    def process_feed_push(
            self,
            request_json
    ):
        Log.info(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Received ' + str(flask.request.method)
            + ' request url "' + str(flask.request.url) + '"'
            + ' from IP ' + str(flask.request.remote_addr)
            + ', JSON: ' + str(request_json)
        )
        try:
            self.feed_queue.put(request_json)
            Log.info(
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Item ' + str(request_json) + ' put to broadcast queue.'
            )
        except Exception as ex_put:
            Log.error(
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Error putting item to queue. Exception: ' + str(ex_put)
                + '. Item: ' + str(request_json)
            )

        # Write to storage (either cache file, memory, DB, etc.)
        self.update_feed_cache(
            feed_json=request_json
        )

        return 'Ok'

    def process_feed_pull(
            self,
            request_json
    ):
        Log.info(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Processing feed pull for request ' + str(request_json)
        )

        # Allow to retrieve feed by some ID
        feed_json = self.get_feed(
            request_json = request_json
        )
        if type(feed_json) in [list, tuple, dict]:
            try:
                retval = json.dumps(feed_json, ensure_ascii=False).encode(encoding=AggregateServer.JSON_ENCODING)
            except Exception as ex_json:
                Log.error(
                    str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                    + ': Error dumping feed json ' + str(feed_json) + ' to json, exception: ' + str(ex_json)
                )
                retval = json.dumps(None)
        else:
            retval = json.dumps(None)

        return retval

    def get_object_persistence(
            self,
            feed_json
    ):
        if self.feed_id_key not in feed_json.keys():
            return None

        feed_id_key = feed_json[self.feed_id_key]
        # Either None or empty string
        if not feed_id_key:
            return None

        obj_file_path = self.feed_cache_folder + '/' + str(feed_id_key) + '.cache'
        lock_file_path = self.feed_cache_folder + '/' + str(feed_id_key) + '.lock'
        objper = ObjectPersistence(
            default_obj    = [],
            obj_file_path  = obj_file_path,
            lock_file_path = lock_file_path
        )
        return objper

    def get_feed(
            self,
            request_json
    ):
        objper = self.get_object_persistence(
            feed_json = request_json
        )
        if objper is None:
            Log.warning(
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': No feed found for ' + str(request_json)
            )
            return False

        feed = objper.read_persistent_object(max_wait_time_secs=1.0)
        return feed

    def update_feed_cache(
            self,
            feed_json
    ):
        objper = self.get_object_persistence(
            feed_json = feed_json
        )
        if objper is None:
            return False

        res = objper.atomic_update(
            new_items = feed_json,
            mode      = ObjectPersistence.ATOMIC_UPDATE_MODE_ADD,
            max_wait_time_secs = 1.0
        )
        Log.info(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Update feed "' + str(feed_json) + '" = ' + str(res)
        )
        return res

    def get_request_json(
            self,
            method = 'POST'
    ):
        req_json = {}
        if method == 'GET':
            for param_name in flask.request.args:
                req_json[param_name] = flask.request.args[param_name]
            return req_json
        else:
            #obj = json.loads(flask.request.json, encoding=AggregateServer.JSON_ENCODING)
            return flask.request.json

    def get_param(self, param_name, method='GET'):
        if method == 'GET':
            if param_name in flask.request.args:
                return str(flask.request.args[param_name])
            else:
                return None
        else:
            try:
                val = flask.request.json[param_name]
                return val
            except Exception as ex:
                Log.critical(
                    str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                    + ': No param name "' + str(param_name) + '" in request.'
                )
                return None

    def run_aggregate_server(
            self,
            host='0.0.0.0'
    ):
        self.app_feed_aggregator.run(
            host     = host,
            port     = self.port
        )


if __name__ == '__main__':
    # One time initialization applies to all modules
    Log.LOGLEVEL = Log.LOG_LEVEL_DEBUG_1
    print(str(__name__) + ': Using log file path "' + str(Log.LOGFILE))
    Log.DEBUG_PRINT_ALL_TO_SCREEN = True

    config = cf.Config.get_cmdline_params_and_init_config_singleton(
        Derived_Class       = cf.Config,
        default_config_file = '/usr/local/git/nwae/nwae.broadcaster/app.data/config/local.cf'
    )

    import queue
    aggregate_server = AggregateServer(
        feed_queue = queue.Queue,
        config     = config
    )
    # If running from gunicorn, no need to run this (will be started by
    # gunicorn instead with host/port given to gunicorn on the command line)
    aggregate_server.run_aggregate_server()
