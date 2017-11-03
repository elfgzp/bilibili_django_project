import logging
import requests
import re
import json
import rsa
import binascii

_logger = logging.getLogger(__name__)


class BilibiliCookieLoader(object):
    __slots__ = ['session', 'cookie', 'success', 'msg']

    def __init__(self, session, user, password, captcha):
        self.session = session
        self.cookie = ''
        self.success = 0
        self.msg = ''
        self.login(user, self.rsaEncrypt(password), captcha)

    def cookie_jar_to_str(self, cookie_jar):
        cookie = ''
        for c in cookie_jar:
            cookie += c.name + '=' + c.value + '; '
        return cookie

    def rsaEncrypt(self, password):
        try:
            token = json.loads(self.session.headers['token'])
            pw = str(token['hash'] + password).encode('utf-8')

            key = token['key']
            key = rsa.PublicKey.load_pkcs1_openssl_pem(key)

            pw = rsa.encrypt(pw, key)
            password = binascii.b2a_base64(pw)
            return password
        except Exception as e:
            _logger.exception(e)
            return False

    def login(self, user, password, captcha):
        post_url = 'https://passport.bilibili.com/login/dologin'
        payload = {
            'act': 'login',
            'gourl': '',
            'keeptime': '2592000',
            'userid': user,
            'pwd': password,
            'vdcode': captcha,
        }
        if not payload["vdcode"]:
            return False

        try:
            response = self.session.post(post_url, data=payload)
            result = re.findall('>\s+(.+)\s+<br', response.text)
            if result:
                self.success = 0
                self.msg = result[0]
            else:
                self.success = 1
                self.msg = '登录成功'
                self.cookie = self.cookie_jar_to_str(self.session.cookies)
        except Exception as e:
            self.msg = e
            return False
        else:
            return True
