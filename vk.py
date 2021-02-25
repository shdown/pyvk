import urllib.request
import urllib.parse
import contextlib
import json
import codecs
import time
import logging


_LOGGER = logging.getLogger('vk')


_MIN_DELAY = 0.36


class VkError(BaseException):
    def __init__(self, obj):
        super().__init__('[{}] {}'.format(obj['error_code'], obj['error_msg']))
        self.code = obj['error_code']
        self.msg = obj['error_msg']
        self.obj = obj


class VkSession:
    def __init__(self, defparams=None):
        self.defparams = defparams or {}
        self.last_req_time = -_MIN_DELAY

    def _update_last_req_time(self):
        now = time.monotonic()
        delay = now - self.last_req_time
        if delay < _MIN_DELAY:
            time.sleep(_MIN_DELAY - delay)
        self.last_req_time = time.monotonic()

    def handle_or_throw(self, err):
        if not isinstance(err, VkError):
            raise err
        if err.code == 6:
            _LOGGER.warning('we are being too fast, sleeping for 3s')
            time.sleep(3)
        elif err.code == 9:
            _LOGGER.warning('we are being too fast, sleeping for 5s')
            time.sleep(5)
        elif code == 1 or code == 10:
            _LOGGER.warning('server unavailable, sleeping for 1s')
            time.sleep(1)
        else:
            raise err

    def request(self, method, params, raw=False):
        all_params = {}
        all_params.update(self.defparams)
        all_params.update(params)
        url = 'https://api.vk.com/method/{}?{}'.format(method, urllib.parse.urlencode(all_params))
        while True:
            self._update_last_req_time()
            _LOGGER.info('making request: method=%s, params=%s', method, params)
            with contextlib.closing(urllib.request.urlopen(url)) as resp:
                obj = json.load(codecs.getreader('utf-8')(resp))
                if raw:
                    return obj
                if 'error' in obj:
                    self.handle_or_throw(VkError(obj['error']))
                return obj['response']

    # Returns (response, error_list).
    def execute(self, params):
        res = self.request('execute', params, raw=True)
        response = res.get('response')
        errors = res.get('execute_errors') or []
        return response, [VkError(obj) for obj in errors]
