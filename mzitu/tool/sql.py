# coding=utf-8
import sqlite3
import logging

logging.basicConfig(level=logging.INFO)

from mzitu.config import sqlite_connect, sqlite_cursor


def init_sql():
    create_download = """create table download
    (
        id         integer  not null,
        link       text     not null,
        title      text     not null,
        category   text     not null,
        date       date     not null
    );"""
    create_error = """create table error
    (
        id         integer  primary key,
        link       text     not null,
        title      text     not null
    );"""
    try:
        sqlite_connect.execute(create_download)
        sqlite_cursor.execute(create_error)
        sqlite_connect.commit()
    except sqlite3.OperationalError:
        logging.info('数据库已经存在')


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


def insert_download(meizi):
    try:
        sqlite_cursor.execute("insert into download (id,link,title,category,date) "
                              "values ('{0}','{1}','{2}','{3}','{4}')"
                              .format(meizi.id, meizi.link, meizi.title, meizi.category, meizi.date))

        sqlite_connect.commit()
    except Exception as e:
        logging.error('插入数据库失败 ' + str(e))


def insert_error(meizi):
    try:
        sqlite_cursor.execute("insert into error (link,title) "
                              "values ('{0}','{1}')"
                              .format(meizi.link, meizi.title))
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
