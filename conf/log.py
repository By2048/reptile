import os
import logging.config
import platform

LOG_PATH = None

if platform.system() == 'Linux':
    # root 权限下运行正常
    # 一些情况下，非root用户没有写入此目录的权限，需要替换成拥有读写权限的用户目录
    LOG_PATH = "/var/log/project/reptile"
elif platform.system() == 'Windows':
    # 将此文件夹路径替换成自己的路径
    LOG_PATH = "E:\\Log\\reptile"

if not os.path.exists(LOG_PATH):
    try:
        os.makedirs(LOG_PATH)
    except Exception as e:
        logging.exception(e)

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "server": {"format": '[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s'},
        "local": {
            "format": '[%(levelname)1.1s %(asctime)s %(module)15s:%(lineno)3d] %(message)s',
            'datefmt': '%H:%M:%S'
        },
        "debug": {
            "format": '[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s',
            'datefmt': '%H:%M:%S'
        }

    },
    "handlers": {
        "local": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "local",
            "stream": "ext://sys.stdout"
        },
        "server": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "formatter": "server",
            "when": "D",
            "interval": 1,
            "filename": os.path.join(LOG_PATH, "service.log")
        },
        "debug": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "debug",
            "stream": "ext://sys.stdout"
        },
    },
    "loggers": {
        "local": {
            "handlers": ["local"],
            "propagate": False
        },
        "server": {
            "handlers": ["server"],
            "propagate": False
        },
        "debug": {
            "handlers": ["debug"],
            "propagate": False
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["local"],
        "propagate": False
    }
}

if __name__ == '__main__':
    logging.config.dictConfig(LOG_CONFIG)
    logging.info('Hello, log')
    logging.getLogger('').info('111')
    logging.getLogger('debug').info('222')
    logging.getLogger('server').info('3333')
