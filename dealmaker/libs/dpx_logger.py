import logging
import logging.config
import yaml


class DpxLogger:

    initialized = False
    _logger = None
    LOGGING_CONFIG = None

    @staticmethod
    def is_init():
        return DpxLogger.initialized

    @staticmethod
    def validate_config():
        if DpxLogger.LOGGING_CONFIG is None:
            return False

        return True

    @staticmethod
    def init():
        if DpxLogger.initialized:
            return DpxLogger._logger

        if DpxLogger.validate_config():
            DpxLogger.initialized = True
            with open(DpxLogger.LOGGING_CONFIG['loggingConfigPath'], 'r') as stream:
                config = yaml.load(stream)

            if config is None:
                raise DpxLoggerInitError('Invalid logging config passed : %s' %
                                         DpxLogger.LOGGING_CONFIG['loggingConfigPath'])
            logging.config.dictConfig(config)
            DpxLogger._logger = logging.getLogger(DpxLogger.LOGGING_CONFIG['loggerName'])

    @staticmethod
    def get_logger():
        if not DpxLogger.initialized:
            raise DpxLoggerInitError('Dpx Logger has not been initiated... use DpxLogger.init() first')

        return DpxLogger._logger


class DpxLoggerInitError (Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
