import logging
from django.http import HttpResponse
import json
import time
from threading import Thread
import requests
import base64
import http.cookiejar as cookielib

from utils.bilibili_cookie_loader import BilibiliCookieLoader

_logger = logging.getLogger(__name__)

bilibili_login_session_cache = {}


def clear_session_cache():
    global bilibili_login_session_cache
    bilibili_login_session_cache = \
        {session_key: bilibili_session
         for session_key, bilibili_session in
         bilibili_login_session_cache
         if bilibili_login_session_cache['time'] - time.time() >= 15}
    time.sleep(15)


clear_session_cache_thread = Thread(target=clear_session_cache, daemon=True)
clear_session_cache_thread.start()


def get_bilibili_cookie(request):
    global bilibili_login_session_cache
    success = 0
    msg = '验证码已过期'
    data = {}
    try:
        if request.method == 'POST':
            bilibili_session = bilibili_login_session_cache.get(request.session.session_key)['session']
            if bilibili_session:
                cookie_loader = BilibiliCookieLoader(
                    bilibili_session,
                    request.POST['user'],
                    request.POST['password'],
                    request.POST['captcha']
                )
                success = cookie_loader.success
                msg = cookie_loader.msg
                data['cookie'] = cookie_loader.cookie
            else:
                msg = '验证码已过期'
    except Exception as e:
        _logger.error(e)
    finally:
        content = {
            'success': success,
            'msg': msg,
            'data': data,
        }

        return HttpResponse(
            content=json.dumps(content),
            content_type='application/json',
            status=200,
            charset='utf-8'
        )


def get_bilibili_captcha(request):
    global bilibili_login_session_cache
    success = 0
    msg = '验证码已过期'
    data = {}
    try:
        request.session['bilibili_session'] = True
        if request.method == 'GET':
            bilibili_session = requests.Session()
            timestamp = int(time.time() * 1000)
            token_url = 'http://passport.bilibili.com/login?act=getkey'
            getKeyRes = bilibili_session.get(token_url)
            captcha_url = 'https://passport.bilibili.com/captcha.gif?r={}&type=login'.format(str(timestamp))
            response = bilibili_session.get(captcha_url)
            bilibili_session.headers['token'] = getKeyRes.content.decode('utf-8')
            base64_img = base64.b64encode(response.content)
            bilibili_login_session_cache[request.session.session_key] = {'session': bilibili_session, 'time': timestamp}
            data['captcha'] = base64_img.decode('utf-8')
    except Exception as e:
        _logger.error(e)
    else:
        success = 1
    finally:
        content = {
            'success': success,
            'msg': msg,
            'data': data,
        }

        return HttpResponse(
            content=json.dumps(content),
            content_type='application/json',
            status=200,
            charset='utf-8'
        )


def proxy(request, base_url, path):
    try:
        request_url = 'http://{}/'.format(base_url) + path
        session = requests.Session()
        session.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cookie': request.META.get('HTTP_SET_COOKIE'),
            'User-Agent': request.META.get('HTTP_USER_AGENT'),
            'Host': base_url,
        }
        response = ''
        if request.method == 'GET':
            payload = request.GET
            response = session.get(request_url, params=payload)
        if request.method == 'POST':
            payload = request.POST
            response = session.post(request_url, data=payload)

        if response:
            response = HttpResponse(
                content=response.content,
                content_type=response.headers['content-type'],
                status=response.status_code,
                reason=response.reason,
                charset=response.encoding,
            )

    except Exception as e:
        _logger.error(e)
        return HttpResponse(
            content=json.dumps('{}'),
            content_type='application/json',
            status=200,
            charset='utf-8'
        )
    else:
        return response


def api_live_bilibili_com(request, path):
    return proxy(request, 'api.live.bilibili.com', path)


def live_bilibili_com(request, path):
    return proxy(request, 'live.bilibili.com', path)

