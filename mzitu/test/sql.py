import sqlite3

from mzitu.config import download_sql_path


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
    con = sqlite3.connect(download_sql_path)
    cur = con.cursor()
    cur.execute(create_download)
    cur.execute(create_error)
    con.commit()
    con.close()


def clear_sql(table='all'):
    con = sqlite3.connect(download_sql_path)
    cur = con.cursor()
    if table == 'all':
        cur.execute('delete from download')
        cur.execute('delete from error')
    elif table == 'download':
        cur.execute('delete from download')
    elif table == 'error':
        cur.execute('delete from download')
    else:
        pass
    con.commit()
    con.close()


def insert_download(meizi):
    con = sqlite3.connect(download_sql_path)
    cur = con.cursor()

    cur.execute("insert into has_down (id,link,title,category,date) "
                "values ('{0}','{1}','{2}','{3}','{4}')"
                .format(meizi.id, meizi.link, meizi.title, meizi.category, meizi.date))

    con.commit()
    con.close()


def insert_error(meizi):
    con = sqlite3.connect(download_sql_path)
    cur = con.cursor()
    cur.execute("insert into error_down (link,title) "
                "values ('{0}','{1}')"
                .format(meizi.link, meizi.title))
    con.commit()
    con.close()


def get_downloads():
    conn = sqlite3.connect(download_sql_path)
    cur = conn.cursor()
    cur.execute("select link from download")
    links = []
    for item in cur.fetchall():
        links.append(item[0])
    return links


def get_errors():
    conn = sqlite3.connect(download_sql_path)
    cur = conn.cursor()
    cur.execute("select link from error")
    links = []
    for item in cur.fetchall():
        links.append(item[0])
    return links


def test():
    pass


if __name__ == '__main__':
    test()
