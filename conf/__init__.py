import logging
from conf import base

from conf.log import LOG_CONFIG

logging.config.dictConfig(LOG_CONFIG)

if __name__ == '__main__':
    print('1', base.MYSQL_HOST)
    print('2', base.MYSQL_HOST)
