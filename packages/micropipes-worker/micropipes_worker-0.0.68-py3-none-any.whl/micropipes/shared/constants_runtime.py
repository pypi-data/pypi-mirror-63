from enum import Enum
import logging

MQ_RUNTIME_EXCHANGE = 'runtime'
MQ_RUNTIME_EXCHANGE_TYPE = 'topic'
MQ_RUNTIME_COLLECTOR_REDIS_QUEUE = 'micropipes.runtime_collector.redis'
MQ_RUNTIME_COLLECTOR_VMETRICS_QUEUE = 'micropipes.runtime_collector.vmetrics'

MQ_RUNTIME_LOGS_ADD = 'runtime.logs.add'
MQ_RUNTIME_STATS_ADD = 'runtime.stats.add'
MQ_RUNTIME_STATS_CUSTOMER_ADD = 'runtime.stats.customer.add'
MQ_RUNTIME_STATS_USAGE_ADD = 'runtime.stats.usage.add'

MQ_RUNTIME_BINDINGS = [MQ_RUNTIME_LOGS_ADD, MQ_RUNTIME_STATS_ADD, MQ_RUNTIME_STATS_CUSTOMER_ADD]
MQ_RUNTIME_BINDINGS_VMETRICS = [MQ_RUNTIME_STATS_USAGE_ADD]


_levelToName = {
    logging.DEBUG: 'DEBUG',
    logging.INFO: 'INFO',
    logging.WARNING: 'WARNING',
    logging.ERROR: 'ERROR',
    logging.CRITICAL: 'CRITICAL'
}

_nameToLevel = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

class LogLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    @staticmethod
    def from_str(level:str):
        return _nameToLevel[level.upper()]

    @staticmethod
    def to_str(level):
        return _levelToName[level]

    @staticmethod
    def log(logger, level, msg):
        if level == LogLevel.DEBUG:
            logger.debug(msg)
        elif level == LogLevel.INFO:
            logger.info(msg)
        elif level == LogLevel.WARNING:
            logger.warning(msg)
        elif level == LogLevel.ERROR:
            logger.error(msg)
        elif level == LogLevel.CRITICAL:
            logger.critical(msg)



STATS_ALL = 'all'
STATS_TIME_KEY = 'time'

# pozor na vyslednu velkost, nasobi sa to poctom precisions, a ops type
STATS_MAX_HISTORY_VALUES = 60

class StatsGroupsKeys(Enum):
    JOB =  'job'
    CUSTOMER = 'customer'

class StatsOutFormatKeys(Enum):
    ARRAY =  'array'
    SERIES = 'series'

class StatsOpsTypes(Enum):
    MIN = 'min'
    MAX = 'max'
    COUNT = 'count'
    SUM = 'sum'
    AVG = 'avg'

STATS_PRECISIONS_FAST_THRESHOLD = 60

STATS_PRECISIONS = {
    '20s': 20,           # 20
    '10m': 10*60,
    '1h': 60*60,
    '1d': 60*60*24
}

STATS_MAINTENANCE_INTERVAL = 60*15
