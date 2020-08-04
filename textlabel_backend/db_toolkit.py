# Name: db_toolkit
# Author: Reacubeth
# Time: 2020/6/23 10:55
# Mail: noverfitting@gmail.com
# Site: www.omegaxyz.com
# *_*coding:utf-8 *_*

import pymysql
import json
import time

# 连接配置信息
config = {
    'host': 'localhost',
    'port': 3306,  # MySQL默认端口
    'user': 'root',  # mysql默认用户名
    'password': '123456',
    'db': 'label_sys',  # 数据库
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}


def db_get_project():
    try:
        con = pymysql.connect(**config)
        sql = "SELECT * FROM project"

        if sql != '':
            with con.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                con.close()
                return result
        else:
            return []
    except Exception:
        return []


def db_delete_project(p_id):
    try:
        con = pymysql.connect(**config)

        sql = "DELETE FROM project WHERE p_id = %s"
        sql2 = "DELETE FROM entity_class WHERE p_id = %s"
        sql3 = "DELETE FROM file WHERE p_id = %s"

        if sql != '':
            with con.cursor() as cursor:
                cursor.execute(sql, p_id)
                cursor.execute(sql2, p_id)
                cursor.execute(sql3, p_id)
                con.commit()
                cursor.close()
                con.close()
                return 'success'
        else:
            return 'error'
    except Exception as e:
        print('Exception: ', e)
        return 'error'


def db_insert_project(p_id, path, name, total):
    try:
        con = pymysql.connect(**config)
        time_str = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))
        sql = "INSERT INTO project(p_id, path, name, time, total) VALUES(%s, %s, %s, %s, %s)"

        if sql != '':
            with con.cursor() as cursor:
                cursor.execute(sql, (p_id, path, name, time_str, total))
                con.commit()
                cursor.close()
                con.close()
                return 'success'
        else:
            return 'error'
    except Exception as e:
        print('Exception: ', e)
        return 'error'


def db_update_project(p_id, file_num):
    try:
        con = pymysql.connect(**config)
        sql = "UPDATE project SET total = total + %s WHERE p_id = %s"

        if sql != '':
            cursor = con.cursor()
            cursor.execute(sql, (file_num, p_id))
            con.commit()
            cursor.close()
            con.close()
            return 'success'
        else:
            return 'error'
    except Exception as e:
        print('Exception: ', e)
        return 'error'


def db_insert_file(name, path, text, p_id):
    try:
        con = pymysql.connect(**config)
        sql = "INSERT INTO file(file_name, file_path, version, entity_list, text, p_id, is_edit) VALUES(%s, %s, %s, %s, %s, %s, %s)"

        if sql != '':
            with con.cursor() as cursor:
                cursor.execute(sql, (name, path, 0, json.dumps([]), text, p_id, 0))
                con.commit()
                cursor.close()
                con.close()
                return 'success'
        else:
            return 'error'
    except Exception as e:
        print('Exception: ', e)
        return 'error'


def db_get_entity_class(p_id):
    try:
        con = pymysql.connect(**config)

        sql = "select * from entity_class where p_id = %s"

        if sql != '':
            with con.cursor() as cursor:
                cursor.execute(sql, p_id)
                result = cursor.fetchall()
                con.close()
                return result
        else:
            return []
    except Exception:
        return []


def db_insert_entity_class(label, color, des, p_id):
    try:
        con = pymysql.connect(**config)

        sql = "INSERT INTO entity_class(label, color, description, p_id) VALUES(%s, %s, %s, %s)"

        if sql != '':
            with con.cursor() as cursor:
                cursor.execute(sql, (label, color, des, p_id))
                con.commit()
                cursor.close()
                con.close()
                return 'success'
        else:
            return 'error'
    except Exception as e:
        print('Exception: ', e)
        return 'error'


def db_update_entity_class(label, color, des, c_id):
    try:
        con = pymysql.connect(**config)
        sql = "UPDATE entity_class SET label=%s, color=%s, description=%s WHERE c_id=%s"

        if sql != '':
            with con.cursor() as cursor:
                cursor.execute(sql, (label, color, des, c_id))
                con.commit()
                cursor.close()
                con.close()
                return 'success'
        else:
            return 'error'
    except Exception as e:
        print('Exception: ', e)
        return 'error'


def db_delete_entity_class(c_id):
    try:
        con = pymysql.connect(**config)

        sql = "DELETE FROM entity_class WHERE c_id = %s"

        if sql != '':
            with con.cursor() as cursor:
                cursor.execute(sql, c_id)
                con.commit()
                cursor.close()
                con.close()
                return 'success'
        else:
            return 'error'
    except Exception as e:
        print('Exception: ', e)
        return 'error'


def db_fetch_file_limit(p_id, anchor, page_size):
    try:
        con = pymysql.connect(**config)
        sql = "SELECT * FROM file where p_id = %s limit %s, %s"

        if sql != '':
            with con.cursor() as cursor:
                cursor.execute(sql, (p_id, anchor, page_size))
                result = cursor.fetchall()
                con.close()
                return result
        else:
            return []
    except Exception:
        return []


def db_update_entity_list(f_id, entity_list):
    try:
        con = pymysql.connect(**config)

        sql = "UPDATE file SET entity_list = %s WHERE f_id = %s"
        sql2 = "UPDATE file SET version = version + 1 WHERE f_id = %s"

        if sql != '':
            cursor = con.cursor()
            cursor.execute(sql, (json.dumps(entity_list), f_id))
            cursor.execute(sql2, f_id)
            con.commit()
            cursor.close()
            con.close()
            return 'success'
        else:
            return 'error'
    except Exception as e:
        print('Exception: ', e)
        return 'error'


def db_change_status(f_id, status):
    try:
        con = pymysql.connect(**config)
        sql = "UPDATE file SET is_edit = %s WHERE f_id = %s"
        if sql != '':
            cursor = con.cursor()
            cursor.execute(sql, (status, f_id))
            con.commit()
            cursor.close()
            con.close()
            return 'success'
        else:
            return 'error'
    except Exception as e:
        print('Exception: ', e)
        return 'error'


if __name__ == '__main__':
    print(db_get_project())
