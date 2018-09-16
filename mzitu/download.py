import os
import sys
import urllib
import logging
import urllib.request
import multiprocessing

import requests

from mzitu.config import download_path, pool_num

logging.basicConfig(level=logging.INFO)


def create_download_path(id: int) -> str:
    """ 创建下载路径

    :param id: 图片的 ID
    :return: image_download_path
    """

    path = os.path.join(download_path, str(id))
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        logging.info('下载路径 {0} 已经存在'.format(path))
    return path


def _download_image(link: str, path: str):
    """ 下载图片

    :param link: 图片的下载链接
    :param path: 图片的保存路径
    :return:
    """

    def call_back(blocknum, blocksize, totalsize):
        """ 下载回显

        :param blocknum: 已经下载的数据块
        :param blocksize: 数据块的大小
        :param totalsize: 远程文件的大小
        :return:
        """
        percent = 100.0 * blocknum * blocksize / totalsize
        sys.stdout.write("\rDownloading : %.2f%%\r" % percent)
        sys.stdout.flush()
        if percent >= 100:
            sys.stdout.write("\rDownloading : %.2f%% -> " % 100)
            print('Download_Success ')

    try:
        urllib.request.urlretrieve(link, path, call_back)
    except Exception as e:
        logging.error("下载失败,下载链接 {0} ".format(link))


def _download_images(links: list, path: str):
    """ 下载一组图片 一个连接下所有图片

    :param links:
    :param path:
    :return:
    """
    pool = multiprocessing.Pool(processes=pool_num)
    for link in links:
        pool.apply_async(_download_image, (link, path))
    pool.close()
    pool.join()


# 使用reqursts下载图片
def download_images(links: list, path: str):
    def get_header(referer: str):
        """ 不添加请求头不能下载

        :param referer: 图片下载链接
        :return: header: 请求头
        """
        header = {
            'Host': 'i.meizitu.net',
            'Pragma': 'no-cache',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) ' +
                           'AppleWebKit/537.36 (KHTML, like Gecko) ' +
                           'Chrome/59.0.3071.115 Safari/537.36'),
            'Accept': 'image-test/webp,image-test/apng,image-test/*,*/*;q=0.8',
            'Referer': '{}'.format(referer),
        }
        return header

    for link in links:
        image_path = os.path.join(path, os.path.basename(link))
        logging.info('下载图片组位置 {0}'.format(image_path))
        try:
            with open(path, "wb+") as file:
                file.write(requests.get(link, headers=get_header(link)).content)
        except Exception as e:
            logging.error('下载图片组位置 {0} 错误 {1}'.format(image_path, str(e)))


if __name__ == '__main__':
    pass
