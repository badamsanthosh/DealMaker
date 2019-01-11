from django.apps import AppConfig
from django.conf import settings
from dealmaker.libs.dpx_logger import DpxLogger
import signal
import sys


class HomeLoansConfig(AppConfig):
    name = 'home_loans'

    def ready(self):
        signal.signal(signal.SIGINT, SignalHandlers.shutdown_handler)
        DpxLogger.LOGGING_CONFIG = settings.DPX_LOGGING_CONFIG
        DpxLogger.init()


class SignalHandlers:

    @staticmethod
    def shutdown_handler(signal=None, frame=None):
        DpxLogger.get_logger().info('Shutting down %s' % HomeLoansConfig.name)
        sys.exit(0)

