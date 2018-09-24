# coding=utf-8
import logging
import pprint

from mzitu.tool.item import MFolder, Meizi
from mzitu.tool.sql import init_sql, get_downloads, get_errors, insert_download
from mzitu.main import get_all_meizi, get_download_links
from mzitu.tool.download import download_images

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    # insert_download(Meizi(1, '2', '3'))
    #
    # pprint.pprint(get_downloads())

    # for mz in get_all_meizi():
    #     mz.info()

    paths = get_download_links('http://i.meizitu.net/2018/09/21b01.jpg', 49)
    # pprint.pprint(paths)

    download_images(paths, '美女秘书美胸挑逗 极品波霸李可可劲爆豪乳遮不住')

