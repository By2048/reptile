"""

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


# 使用主页下载图片
max_page_num=get_max_page_num()
max_page_num = 5
for page_num in range(max_page_num):
    meizi_links = get_meizi_link_in_start_page(page_num + 1)
"""