from django.conf import settings
import re
from rest_framework.response import Response
from rest_framework import status, serializers
from dealmaker import DpxLogger
from Crypto import Random
from Crypto.Cipher import AES
import base64
from datetime import timedelta
from django.utils.timezone import localtime
from rest_framework_jwt.utils import *
import time
import jwt


class AuthUtil:

    @staticmethod
    def encrypt(payload):
        bs = 16
        pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
        iv = Random.new().read(bs)
        aes = AES.new(settings.AES_SECRET_KEY.encode("utf-8"),
                      AES.MODE_CBC,
                      iv)
        return base64.b64encode(
            aes.encrypt(pad(payload).encode("utf-8")) + iv
        )

    @staticmethod
    def decrypt(payload):
        unpad = lambda s: s[:-ord(s[len(s)-1:])]
        payload = base64.b64decode(payload)
        iv = payload[-16:]
        payload = payload[:-16]
        aes = AES.new(settings.AES_SECRET_KEY.encode("utf-8"),
                      AES.MODE_CBC,
                      iv)
        return unpad(aes.decrypt(payload)).decode("utf-8")

    @staticmethod
    def verify_expiration(expiry_ts, refresh_limit):
        try:
            if isinstance(refresh_limit, timedelta):
                refresh_limit = (refresh_limit.days * 24 * 3600 + refresh_limit.seconds)
            expiration_timestamp = expiry_ts + int(refresh_limit)
            now_timestamp = time.mktime(localtime().timetuple())
            if now_timestamp > expiration_timestamp:
                return False
            return True
        except Exception as e:
            DpxLogger.get_logger().error("Unable to validate Original IAT expiration")
            DpxLogger.get_logger().error(e)

    @staticmethod
    def get_payload(aes_decrypted_token):
        try:
            decoded_claims = jwt_decode_handler(aes_decrypted_token) # ORIG IAT is handled here.
            return decoded_claims
        except jwt.ExpiredSignature:
            msg = _('Signature has expired.')
            raise serializers.ValidationError(msg)
        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            raise serializers.ValidationError(msg)

    @staticmethod
    def get_token_content(token_payload):
        try:
            DpxLogger.get_logger().debug(" Auth Utils : get_token_content: Enter. token payload %s " % token_payload)
            decrypted_token = AuthUtil.decrypt(token_payload)
            payload_info = AuthUtil.get_payload(decrypted_token)
            if payload_info:
                iat = payload_info['iat']
                is_iat_valid = AuthUtil.verify_expiration(iat, api_settings.JWT_EXPIRATION_DELTA)
                if is_iat_valid:
                    return payload_info
            return False

        except BaseException as e:
            DpxLogger.get_logger().error(str(e))
            return False


def get_auth_header(*args, **kwargs):
    if 'HTTP_AUTHORIZATION' not in args[0].parser_context['request'].META:
        DpxLogger.get_logger().error('Auth token is missing')
        return None
    auth = args[0].parser_context['request'].META['HTTP_AUTHORIZATION']
    return auth


def l_replace(pattern, sub, string):
    return re.sub('^%s' % pattern, sub, string)


# DPX Auth Decorator
def dpx_authenticator(function):
    def wrap(request, *args, **kwargs):
        auth_from_request = get_auth_header(*args, **kwargs)
        if auth_from_request is None:
            DpxLogger.get_logger().error('User is not authenticated')
            return Response('User is not authenticated', status=status.HTTP_401_UNAUTHORIZED)
        DpxLogger.get_logger().debug(auth_from_request)
        auth_token = l_replace('JWT ', '', auth_from_request)
        token_claims = AuthUtil.get_token_content(auth_token)
        if not token_claims:
            return Response('Invalid Token or token expired', status=status.HTTP_401_UNAUTHORIZED)
        args = list(args)
        args.append(token_claims['user'])
        return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
