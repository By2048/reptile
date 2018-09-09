# Time 2017-2-1
import json
import urllib.request
import sys
import os
import shutil

from config import keep_path, temp_path


class BImage:
    def __init__(self, date, link, title):
        self.date = date
        self.link = link
        self.title = title


def call_back(blocknum, blocksize, totalsize):
    """下载回显
    Args:
       blocknum: 已经下载的数据块
       blocksize: 数据块的大小
       totalsize: 远程文件的大小
    """
    percent = 100.0 * blocknum * blocksize / totalsize
    sys.stdout.write("\rDownloading : %.2f%%\r" % percent)
    sys.stdout.flush()
    if percent >= 100:
        sys.stdout.write("\rDownloading : %.2f%% -> " % 100)
        print('Download_Success ')

# api detail link = http://stackoverflow.com/questions/10639914/is-there-a-way-to-get-bings-photo-of-the-day
# api = 'http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US'


def get_image(idx, n):  # idx=0,n=1
    api_url = 'http://www.bing.com/HPImageArchive.aspx?format=js&idx=' + \
        str(idx) + '&n=' + str(n) + '&mkt=en-US'
    data = urllib.request.urlopen(api_url).read().decode('utf-8')
    BImages = []
    json_data = json.loads(data)
    for i in range(n):
        _date = json_data['images'][i]['enddate']
        _title = json_data['images'][i]['copyright'].replace('/', ' ')
        _link = 'http://www.bing.com' + json_data['images'][i]['url']
        BImages.append(BImage(_date, _link, _title))
    return BImages


def get_image_name(image):
    image_name = image.date[0:4]+"-"+image.date[4:6]+"-"+image.date[6:8]\
        + " "\
        + image.title \
        + '.' \
        + image.link.split('.')[-1]
    return image_name


def create_temp_jpg(img_path):
    if os.path.exists(img_path) == False:
        with open(img_path, 'w') as file:
            file.close()


if __name__ == '__main__':
    print('\nStart')
    images = get_image(idx=0, n=7)
    image_path = ""
    create_temp_jpg(temp_path)
    for image in images:
        image_path = os.path.join(keep_path, get_image_name(image))
        if os.path.isfile(image_path):
            pass
            # print('\n' + image-test.title + '\n' + image-test.link)
            # print('Has been downloaded')
        else:
            print('\n' + image.title + '\n' + image.link)
            urllib.request.urlretrieve(image.link, image_path, call_back)
            shutil.copy(image_path, temp_path)

    # os.system("start {0}".format(temp_path))  # win 环境下使用默认的图片浏览器打开今日图片
    print('\nEnd')
