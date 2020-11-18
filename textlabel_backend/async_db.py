# Name: async_db
# Author: Reacubeth
# Time: 2020/8/10 16:38
# Mail: noverfitting@gmail.com
# Site: www.omegaxyz.com
# *_*coding:utf-8 *_*

import json
import time
import aiomysql

POOL = {}

Cursor = aiomysql.Cursor
DictCursor = aiomysql.DictCursor
SSCursor = aiomysql.SSCursor
SSDictCursor = aiomysql.SSDictCursor


async def get_pool(db):
    global POOL
    if db not in POOL:
        POOL[db] = await aiomysql.create_pool(
            maxsize=20,
            host='localhost',
            port=3306,
            user='root',
            password='123456',
            db=db,
            charset='utf8mb4',
            autocommit=True
        )
    return POOL[db]


async def mysql_select(sql, *params, db, cursor_type=Cursor):
    pool = await get_pool(db)
    async with pool.acquire() as conn:
        async with conn.cursor(cursor_type) as cursor:
            await cursor.execute(sql, params)
            return await cursor.fetchall()


async def get_project():
    sql = "SELECT * FROM project"
    ret = await mysql_select(sql, db='label_sys', cursor_type=DictCursor)
    return ret


async def delete_project(p_id):
    sql = "DELETE FROM project WHERE p_id = %s"
    sql2 = "DELETE FROM entity_class WHERE p_id = %s"
    sql3 = "DELETE FROM file WHERE p_id = %s"
    ret = await mysql_select(sql, p_id, db='label_sys')
    ret2 = await mysql_select(sql2, p_id, db='label_sys')
    ret3 = await mysql_select(sql3, p_id, db='label_sys')
    return 'success'


async def insert_project(p_id, path, name, total):
    time_str = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))
    sql = "INSERT INTO project(p_id, path, name, time, total) VALUES(%s, %s, %s, %s, %s)"
    ret = await mysql_select(sql, p_id, path, name, time_str, total, db='label_sys')
    return 'success'


async def update_project(p_id, file_num):
    sql = "UPDATE project SET total = total + %s WHERE p_id = %s"
    ret = await mysql_select(sql, file_num, p_id, db='label_sys')
    return 'success'


async def insert_file(name, path, text, p_id, entity_list, hint):
    sql = "INSERT INTO file(file_name, file_path, version, entity_list, text, p_id, is_edit, hint, Mark_relation) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    ret = await mysql_select(sql, name, path, 0, json.dumps(entity_list), json.dumps(text), p_id, 0, json.dumps(hint), json.dumps(eval('[]')), db='label_sys')
    return 'success'


async def get_entity_class(p_id):
    sql = "select * from entity_class where p_id = %s"
    ret = await mysql_select(sql, p_id, db='label_sys', cursor_type=DictCursor)
    return ret


async def insert_entity_class(label, color, des, p_id):
    sql = "INSERT INTO entity_class(label, color, description, p_id) VALUES(%s, %s, %s, %s)"
    ret = await mysql_select(sql, label, color, des, p_id, db='label_sys')
    return 'success'


async def update_entity_class(label, color, des, c_id):
    sql = "UPDATE entity_class SET label=%s, color=%s, description=%s WHERE c_id=%s"
    ret = await mysql_select(sql, label, color, des, c_id, db='label_sys')
    return 'success'


async def delete_entity_class(c_id):
    sql = "DELETE FROM entity_class WHERE c_id = %s"
    ret = await mysql_select(sql, c_id, db='label_sys')
    return 'success'


async def fetch_file_limit(p_id, anchor, page_size):
    sql = "SELECT * FROM file where p_id = %s limit %s, %s"
    ret = await mysql_select(sql, p_id, anchor, page_size, db='label_sys', cursor_type=DictCursor)
    return ret


async def update_entity_list(f_id, entity_list):
    sql = "UPDATE file SET entity_list = %s WHERE f_id = %s"
    sql2 = "UPDATE file SET version = version + 1 WHERE f_id = %s"
    ret = await mysql_select(sql, json.dumps(entity_list), f_id, db='label_sys')
    ret2 = await mysql_select(sql2, f_id, db='label_sys')

    sql_log = "INSERT INTO project_history(f_id, p_id, version, entity_list, Mark_relation) select f_id, p_id, version, entity_list, Mark_relation from file where f_id = %s"
    ret_log = await mysql_select(sql_log, f_id, db='label_sys')
    return 'success'


async def update_relation_list(f_id, relation_list):
    sql = "UPDATE file SET Mark_relation = %s WHERE f_id = %s"
    ret = await mysql_select(sql, json.dumps(relation_list), f_id, db='label_sys')
    return 'success'


async def change_status(f_id, status):
    sql = "UPDATE file SET is_edit = %s WHERE f_id = %s"
    ret = await mysql_select(sql, status, f_id, db='label_sys')
    return 'success'


async def get_figure_class():
    sql = "select * from figure_class"
    ret = await mysql_select(sql, db='label_sys', cursor_type=DictCursor)
    return ret


async def get_rand_figure():
    sql = "select * from figure ORDER BY rand() limit 1"
    ret = await mysql_select(sql, db='label_sys', cursor_type=DictCursor)
    return ret


async def get_figure(figure_id):
    sql = "select * from figure WHERE figure_id = %s"
    ret = await mysql_select(sql, figure_id, db='label_sys', cursor_type=DictCursor)
    return ret


async def update_figure_class(figure_id, figure_c):
    sql = "UPDATE figure SET label = %s WHERE figure_id = %s"
    sql2 = "UPDATE figure SET version = version + 1 WHERE figure_id = %s"
    ret = await mysql_select(sql, figure_c, figure_id, db='label_sys')
    ret2 = await mysql_select(sql2, figure_id, db='label_sys')
    return 'success'


async def insert_figure_class(label, color):
    sql = "INSERT INTO figure_class(label, color) VALUES(%s, %s)"
    ret = await mysql_select(sql, label, color, db='label_sys')
    return 'success'

