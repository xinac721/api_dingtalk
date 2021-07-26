import json

from django.http import HttpResponse

from xtools.dingtalk import DingTalkUtils


def index(request):
    access_token = None
    message = None
    secret = None
    keyword = None
    if request.method == 'GET':
        access_token, message, secret, keyword = _get(request)
    elif request.method == 'POST':
        access_token, message, secret, keyword = _post(request)
    result_code = 0
    result_msg = 'ok'
    if access_token and message:
        if secret:
            # 签名消息
            result = DingTalkUtils.send_sign_msg(message, access_token, secret)
            if result:
                result_code = result[0]
                result_msg = result[1]
            pass
        elif keyword:
            # 关键字消息
            result = DingTalkUtils.send_msg(message, access_token, keyword)
            if result:
                result_code = result[0]
                result_msg = result[1]
            pass
        else:
            # IP类型消息，暂不支持
            pass
    else:
        result_code = '-1'
        result_msg = 'Usage: ?token=token&text=text&keyword=[keyword]&secret=[secret]'

    data = {'result': result_code, 'msg': result_msg, 'ver': '1.0', 'author': 'https://api.xinac.net'}
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json; charset=utf-8')


def _get(request):
    id = request.GET.get('id')
    token = request.GET.get('token')
    access_token = request.GET.get('access_token')
    if not access_token:
        if token:
            access_token = token
        elif id:
            access_token = id
        else:
            pass
    msg = request.GET.get('msg')
    text = request.GET.get('text')
    content = request.GET.get('content')
    message = request.GET.get('message')
    if not message:
        if content:
            message = content
        elif text:
            message = text
        elif msg:
            message = msg
        else:
            pass

    keyword = request.GET.get('keyword')
    secret = request.GET.get('secret')
    return access_token, message, secret, keyword


def _post(request):
    id = request.POST.get('id')
    token = request.POST.get('token')
    access_token = request.POST.get('access_token')
    if not access_token:
        if token:
            access_token = token
        elif id:
            access_token = id
        else:
            pass
    msg = request.POST.get('msg')
    text = request.POST.get('text')
    content = request.POST.get('content')
    message = request.POST.get('message')
    if not message:
        if content:
            message = content
        elif text:
            message = text
        elif msg:
            message = msg
        else:
            pass

    keyword = request.POST.get('keyword')
    secret = request.POST.get('secret')
    return access_token, message, secret, keyword
