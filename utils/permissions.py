from rest_framework import status
from rest_framework.response import Response


def is_authorized(group_name):
    def auth_decorator(function):
        def wrap(request, *args, **kwargs):
            pay_load = args[1]
            user_id = -1
            if "user_id" in request.request.data:
                user_id = int(request.request.data.get('user_id'))
            if pay_load.get('is_admin') or \
                    (pay_load['groups'].get(group_name) == 'admin') or \
                    pay_load.get('user_id') == user_id:
                return function(request, *args, **kwargs)
            else:
                return Response("User is not authorised", status=status.HTTP_401_UNAUTHORIZED)
        return wrap
    return auth_decorator


def is_owner(function):
    def wrap(request, *args, **kwargs):
        pay_load = args[1]
        user_id = int(kwargs.get('pk') or 0)
        if "user_id" in request.request.data:
            user_id = int(request.request.data.get('user_id'))
        if pay_load.get('is_admin') or user_id == pay_load.get('user_id'):
            return function(request, *args, **kwargs)
        else:
            return Response("User is not authorised", status=status.HTTP_401_UNAUTHORIZED)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
