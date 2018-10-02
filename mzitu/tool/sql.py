# coding=utf-8
import sqlite3
import logging

from mzitu.config import sqlite_connect, sqlite_cursor
from mzitu.tool.item import Meizi, MFolder, MImage
from mzitu.config import download_sql_path, download_txt_path

logging.basicConfig(level=logging.INFO)


def init_sql():
    connect = sqlite3.connect(download_sql_path)
    cursor = connect.cursor()
    create_download = """create table download
    (
        id         integer  not null,
        link       text     not null,
        name       text     not null,
        category   text     not null,
        date       date     not null,
        downloads  text     not null
    );"""
    create_error = """create table error
    (
        id         integer  primary key,
        link       text     not null,
        name       text     not null
    );"""
    try:
        cursor.execute(create_download)
        cursor.execute(create_error)
        connect.commit()
    except Exception as e:
        logging.info('数据库初始化失败{}'.format(str(e)))
    finally:
        connect.close()

    with open(download_txt_path, 'w') as file:
        file.close()


def clear_sql(table='all'):
    try:
        if table == 'all':
            sqlite_cursor.execute('delete from download')
            sqlite_cursor.execute('delete from error')
        elif table == 'download':
            sqlite_cursor.execute('delete from download')
        elif table == 'error':
            sqlite_cursor.execute('delete from download')
        sqlite_connect.commit()
    except Exception as e:
        logging.error('清除数据库失败 ' + str(e))


def insert_download(meizi: Meizi):
    try:
        insert = "insert into download (id,link,name,category,date,downloads) "
        fmt = "values ('{0}','{1}','{2}','{3}','{4}','{5}')"
        param = [meizi.id, meizi.link, meizi.name, meizi.category, meizi.date, ','.join(meizi.downloads)]
        sqlite_cursor.execute(insert + fmt.format(*param))
        sqlite_connect.commit()
    except Exception as e:
        logging.error('插入数据库失败 ' + str(e))

    try:
        with open(download_txt_path, 'a', encoding='utf-8') as file:
            file.write(str(meizi).strip() + '\n')
    except Exception as e:
        logging.error('写入文件失败 ' + str(e))


def insert_error(meizi: Meizi):
    try:
        insert = "insert into error (link,name) "
        fmt = "values ('{0}','{1}')"
        param = [meizi.link, meizi.name]
        sqlite_cursor.execute(insert + fmt.format(*param))
        sqlite_connect.commit()
    except Exception as e:
        logging.error('插入数据库失败 ' + str(e))


def get_downloads():
    sqlite_cursor.execute("select link from download")
    downloads = []
    for item in sqlite_cursor.fetchall():
        downloads.append(item[0])
    return downloads


def get_errors():
    sqlite_cursor.execute("select link from error")
    errors = []
    for item in sqlite_cursor.fetchall():
        errors.append(item[0])
    return errors


if __name__ == '__main__':
    pass
