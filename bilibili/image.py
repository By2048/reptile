class bili_img:
    # name 图片名
    # down_link 下载链接
    # author 作者
    # detail_link 图片详情页
    # num 图片数量
    # create_date 上传事件
    # category 分类
    # tag 标签
    # character_name 角色名
    # source 来源
    # discription 详细信息

    def __init__(self,name,down_link,author,detail_link,num,create_date,
                 category,tag,character_name,source,discription):
        self.name=name
        self.down_link=down_link
        self.author=author
        self.detail_link=detail_link
        self.num=num
        self.create_date=create_date
        self.category=category
        self.tag=tag
        self.character_name=character_name
        self.source=source
        self.discription=discription

    def print_first(self):
        print('name'.ljust(20,' ')+self.name[0])
        print('down_link'.ljust(20,' ')+self.down_link[0])
        print('author'.ljust(20,' ')+str(self.author))
        print('detail_link'.ljust(20,' ')+self.detail_link)
        print()

    def print_all(self):
        if len(self.name)==1:
            print('name'.ljust(20,' ')+self.name[0])
        else:
            print('name'.ljust(20, ' '),end='')
            print(self.name)
        if len(self.down_link)==1:
            print('down_link'.ljust(20,' ')+self.down_link[0])
        else:
            print('down_link'.ljust(20,' '),end='')
            print(self.down_link)
        print('author'.ljust(20,' ')+str(self.author))
        print('detail_link'.ljust(20,' ')+self.detail_link)
        print('num'.ljust(20,' ')+str(self.num))
        print('create_date'.ljust(20,' ')+str(self.create_date))
        print('category'.ljust(20,' ')+str(self.category))
        print('tag'.ljust(20,' ')+str(self.tag))
        print('character_name'.ljust(20,' ')+str(self.character_name))
        print('source'.ljust(20,' ')+str(self.source))
        print('discription'.ljust(20,' ')+repr(self.discription))
        print()
