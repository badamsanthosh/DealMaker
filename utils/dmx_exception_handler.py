from rest_framework.views import exception_handler, Response
from rest_framework import status

from dealmaker.libs.dpx_logger import DpxLogger


def custom_drf_exception(exc, context):
    DpxLogger.get_logger().error(exc)
    response = exception_handler(exc, context)
    if response is not None:
        response.data['status_code'] = response.status_code

    else:
        if isinstance(exc, ValueError):
            data = "Not a valid request"
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = "Internal Server Error"
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response


