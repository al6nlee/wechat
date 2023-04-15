import pymysql

from src.utils.conf_section import get_conf_section

config = {'host': get_conf_section("MYSQL", "HOST"),
          'port': int(get_conf_section("MYSQL", "PORT")),
          'user': get_conf_section("MYSQL", "USER"),
          'passwd': get_conf_section("MYSQL", "PASSWORD"),
          'db': get_conf_section("MYSQL", "DB")
          }


def query_sql(sql, params):
    pass


def insert_sql(sql, params):
    print(sql % params)
    conn = pymysql.connect(**config)
    # 打开游标
    cur = conn.cursor()
    ret = False
    obj_id = ""
    # 编写sql语句
    try:
        # 执行sql语句
        cur.execute(sql, params)
        conn.commit()
        obj_id = cur.lastrowid
        ret = True
    except Exception as err:
        print(err)
        conn.rollback()
    print('数据增加成功')
    # 关闭游标
    cur.close()
    # 关闭连接
    conn.close()
    return ret, obj_id


def update_sql(sql, params):
    print(sql % params)
    conn = pymysql.connect(**config)
    # 打开游标
    cur = conn.cursor()
    ret = False
    obj_id = ""
    # 编写sql语句
    try:
        # 执行sql语句
        cur.execute(sql, params)
        conn.commit()
        obj_id = cur.lastrowid
        ret = True
    except Exception as err:
        print(err)
        conn.rollback()
    print('更新数据成功')
    # 关闭游标
    cur.close()
    # 关闭连接
    conn.close()
    return ret, obj_id
