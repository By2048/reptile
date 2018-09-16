import os
import sys
import socket
import logging
import multiprocessing

import pymysql

logging.basicConfig(level=logging.INFO)

socket.setdefaulttimeout(10)

pool_num = multiprocessing.cpu_count()

if sys.platform == 'linux':
    download_path = '/home/am/Pictures/mzitu'
elif sys.platform == 'win32':
    download_path = r'F:\Image\mzitu'
else:
    raise Exception('获取下载路径出错')

download_txt_path = os.path.join(download_path, 'download.txt')

download_sql_path = os.path.join(download_path, 'download.db')

user_agent = ('Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
              'AppleWebKit/537.36 (KHTML, like Gecko)'
              'Chrome/53.0.2785.143 Safari/537.36')

header = {'User-Agent': user_agent}

images_link = 'http://www.mzitu.com/all'

start_link = 'http://www.mzitu.com'

try:
    mysql_con_text = pymysql.connect(
        host="localhost",
        user="root",
        passwd="admin",
        db="mzitu",
        use_unicode=True,
        charset="utf8"
    )
except Exception as e:
    logging.error(str(e))

if __name__ == '__main__':
    logging.info("{0:<15}{1}".format('keep_path', download_path))
    logging.info("{0:<15}{1}".format('user_agent', user_agent))
    logging.info("{0:<15}{1}".format('header', header))
    logging.info("{0:<1}{1}".format('images_link', images_link))
    logging.info("{0:<15}{1}".format('start_link', start_link))
    logging.info("{0:<20}{1}".format('download_txt_path', download_txt_path))
    logging.info("{0:<20}{1}".format('download_sql_path', download_sql_path))
