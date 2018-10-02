# coding=utf-8
import os
import time
import datetime
import logging

import requests
from bs4 import BeautifulSoup

from mzitu.config import images_link, headers
from mzitu.tool.sql import get_downloads, insert_download, insert_error
from mzitu.tool.download import download_images
from mzitu.tool.image import change_name, get_folder_info
from mzitu.tool.item import MImage, MFolder, Meizi
from mzitu.tool.download import download_images

from mzitu.config import download_txt_path

logging.basicConfig(level=logging.INFO)


def get_meizi_other_info(meizi):
    # 获取图片的其他信息
    def get_image_num(soup):
        """ 获取一个页面的最大图片数量 方便合成连接

        :param soup:
        :return:
        """
        max_num = 0
        try:
            for span in soup.find('div', class_='pagenavi').find_all('span'):
                if (span.get_text() == '下一页»'):
                    max_num = span.parent.previous_sibling.find('span').get_text()
        except Exception as e:
            logging.error('获取最大数量图片失败 ' + str(e))
        finally:
            return int(max_num)

    def get_first_img_down_link(soup):
        """ 获取第一张图片下载的连接

        :param soup:
        :return:
        """
        link = None
        try:
            link = soup.find('div', class_='main-image').find('img')['src']
        except Exception as e:
            logging.error('get img link fail ' + str(e))
        finally:
            return link

    def get_categroy_date(soup):
        """ 获取图片的 分类 日期

        :param soup:
        :return:
        """
        category, date = None, None
        try:
            spans = soup.find('div', class_='main-meta').find_all('span')
            category = spans[0].find('a').get_text()
            date = spans[1].get_text().replace('发布于 ', '')
        except Exception as e:
            logging.error('get category date fail ' + str(e))
        finally:
            return category, date

    def get_download_links(download_link, max_num):
        """ 通过字符串合成的方式获取下载链接              \n
        http://i.meizitu.net/2017/10/29c02.jpg          \n
        start_link   http://i.meizitu.net/2017/10       \n
        image_name   29c02.jpg                          \n
        _name        29c                                \n
        _num         02                                 \n
        _type        jpg                                \n
        """
        start_link, image_name = os.path.split(download_link)

        _name = image_name.split('.')[0][:-2]
        _num = int(image_name.split('.')[0][-2:])
        _type = image_name.split('.')[1]

        downloads = []
        for num in range(_num, _num + max_num):
            fmt = '{start_link}/{name}{num}.{type}'
            downloads.append(fmt.format(start_link=start_link, name=_name, num=str(num).zfill(2), type=_type))
        logging.info('image_start_link  :  {}'.format(download_link))
        logging.info('image_max_num     :  {}'.format(max_num))
        return downloads

    try:
        html = requests.get(meizi.link, headers=headers)
        soup = BeautifulSoup(html.text, "html.parser")
        max_num = get_image_num(soup)
        first_down_link = get_first_img_down_link(soup)
        meizi.category, meizi.date = get_categroy_date(soup)
        meizi.downloads = get_download_links(first_down_link, max_num)
    except Exception as e:
        logging.info('获取图片其他信息失败{}'.format(e))
    finally:
        return meizi


def get_all_meizi():
    """ 获取 http://www.mzitu.com/all/ 下数据

    :return: [Meizi(_id, _title, _link, _category, _date)]
    """
    meizis, soup = [], None
    try:
        html = requests.get(images_link, headers=headers)
        soup = BeautifulSoup(html.text, "html.parser")
    except Exception as e:
        logging.error('获取{}网页失败{}'.format(images_link, str(e)))
    try:
        for ul in soup.find_all('ul', class_='archives'):
            for link in ul.find_all('a'):
                _id = link['href'].split('/')[-1]
                _title = link.get_text()
                _link = link['href']
                _category, _date = '', ''
                meizis.append(Meizi(_id, _title, _link, _category, _date))
    except Exception as e:
        logging.error('解析{}失败{} '.format(images_link, str(e)))
    finally:
        return meizis


# 主程序
def main():
    downloads = get_downloads()

    meizis = get_all_meizi()
    for meizi in meizis:
        if meizi.link not in downloads:
            try:
                logging.info('name              :  {}'.format(meizi.name))
                meizi = get_meizi_other_info(meizi)
                download_images(meizi.id, meizi.name, meizi.downloads)
                insert_download(meizi)
            except Exception as e:
                logging.error('失败 {}'.format(str(e)))
                insert_error(meizi)
            finally:
                time.sleep(9)


if __name__ == '__main__':
    """
    INFO:root:title 深宅大院中的姨太太 万种风情,千般风流                         link http://www.mzitu.com/152431                      
    INFO:root:获取图片其他信息失败'start_link'
    """
    mz = Meizi('152431', '深宅大院中的姨太太 万种风情,千般风流', 'http://www.mzitu.com/152431')

    with open(download_txt_path, 'a', encoding='utf-8') as file:
        file.write(str(mz).strip() + '\n')
