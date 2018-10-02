# coding=utf-8
import os
import time
import logging
import datetime

from mzitu.main import main
from mzitu.tool.sql import init_sql
from mzitu.config import download_txt_path, download_sql_path, download_path

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':

    logging.info('start mzitu         {}'.format(datetime.datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')))
    logging.info('download_path       {}'.format(download_path))
    logging.info('download_sql_path   {}'.format(download_sql_path))

    if not os.path.isfile(download_txt_path):
        init_sql()

    main()

    logging.info('---- end ----')
