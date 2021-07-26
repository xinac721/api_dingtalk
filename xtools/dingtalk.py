# -*- coding: utf-8 -*-

import base64
import hashlib
import hmac
import json
import os
import sys
import time
import urllib.parse

import requests

from xtools import header

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


def hmac_sign(secret):
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return timestamp, sign


class DingTalkUtils:
    NOTIFY_NONE = 0
    NOTIFY_DINGTALK = 1

    _dingtalk_api = 'https://oapi.dingtalk.com/robot/send?access_token'

    def __init__(self):
        pass

    @staticmethod
    def send_msg(content, access_token, keyword):
        data = dict()
        data['msgtype'] = 'text'
        data['text'] = dict()
        data['text']['content'] = '[{}]'.format(keyword) + '\n' + content

        headers = header.get_header()
        headers['Content-Type'] = 'application/json; charset=utf-8'
        _api_url = '='.join([DingTalkUtils._dingtalk_api, access_token])

        resp = requests.post(_api_url, headers=headers,
                             data=json.dumps(data, ensure_ascii=False).encode("utf-8"))

        print('---> ', resp.content)
        resp_json = json.loads(resp.content.decode('utf-8', 'ignore'))
        return resp_json['errcode'], resp_json['errmsg']

    @staticmethod
    def send_sign_msg(content, access_token, secret):
        if content and secret and access_token:
            timestamp, sign = hmac_sign(secret)
            data = dict()
            data['msgtype'] = 'text'
            data['text'] = dict()
            data['text']['content'] = content

            headers = header.get_header()
            headers['Content-Type'] = 'application/json; charset=utf-8'
            _api_url = '='.join([DingTalkUtils._dingtalk_api, access_token])
            _api_url = '&'.join([_api_url, 'timestamp'])
            _api_url = '='.join([_api_url, timestamp])
            _api_url = '&'.join([_api_url, 'sign'])
            _api_url = '='.join([_api_url, sign])

            resp = requests.post(_api_url, headers=headers,
                                 data=json.dumps(data, ensure_ascii=False).encode("utf-8"))
            print('---> ', resp.content)
            resp_json = json.loads(resp.content.decode('utf-8', 'ignore'))
            return resp_json['errcode'], resp_json['errmsg']
        else:
            return None
        pass

# if __name__ == "__main__":
#     pass
