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


def get_other_info(detail_link):
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

    max_num, first_down_link, category, date = None, None, None, None
    try:
        html = requests.get(detail_link, headers=headers)
        soup = BeautifulSoup(html.text, "html.parser")
        max_num = get_image_num(soup)
        first_down_link = get_first_img_down_link(soup)
        category, date = get_categroy_date(soup)
    except Exception as e:
        print('获取图片其他信息失败' + str(e))
    finally:
        return max_num, first_down_link, category, date


#  获取第一张图片的下载地址 根据下载地址合成其他下载连接
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
        downloads.append('{start_link}/{name}{num}.{type}'.
                         format(start_link=start_link, name=_name, num=str(num).zfill(2), type=_type))
    return downloads


def get_all_meizi():
    """ 获取 http://www.mzitu.com/all/ 下数据

    :return: [Meizi(_id, _title, _link, _category, _date)]
    """
    meizis = []
    try:
        html = requests.get(images_link, headers=headers)
        soup = BeautifulSoup(html.text, "html.parser")
        for ul in soup.find_all('ul', class_='archives'):
            for link in ul.find_all('a'):
                _id = link['href'].split('/')[-1]
                _title = link.get_text()
                _link = link['href']
                _category, _date = '', ''
                meizis.append(Meizi(_id, _title, _link, _category, _date))
    except Exception as e:
        logging.error('获取所有下载链接失败 ' + str(e))
    finally:
        return meizis


# 获取开始页面每页中所有的图片的详细连接
def get_meizi_link_in_start_page(page_num):
    page_link = 'http://www.mzitu.com/page/' + str(page_num)
    html = requests.get(page_link, headers=headers)
    soup = BeautifulSoup(html.text, "html.parser")
    meizi_links = []
    for li in soup.find('ul', id='pins').find_all('li'):
        link = li.find('span').find('a')
        tmp = Meizi(change_name(link.get_text()), link['href'])
        meizi_links.append(tmp)
    return meizi_links


# 主程序
def main():
    print('\nStart')
    downloads = get_downloads()
    """
    # 使用主页下载图片
    max_page_num=get_max_page_num()
    max_page_num = 5
    for page_num in range(max_page_num):
        meizi_links = get_meizi_link_in_start_page(page_num + 1)
    """
    all_meizi = get_all_meizi()
    for meizi in all_meizi:
        if meizi.link not in downloads:
            meizi.info()
            try:
                max_num, first_down_link, category, date = get_other_info(meizi.link)
                meizi.category, meizi.date = category, date
                download_links = get_download_links(first_down_link, max_num)
                logging.info('image_start_link  :  {0}\nimage_max_num     :  {1}'
                             .format(download_links[0], str(max_num)))
                download_images(download_links, meizi.title)
                insert_download(meizi)
                time.sleep(5)
            except:
                insert_error(meizi)
            print()
    logging.info('---- end ----')


if __name__ == '__main__':
    pass
