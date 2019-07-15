# -*- coding:utf-8 -*-

import pymongo
from mod.tools.check import Check

class MongoDB(object):
    """
    针对 MongoDB 操作的类
    """
    mongo_conn = None

    def __init__(self):
        """
        :return MongoDB Client Session
        """
        mongo_url = Check.get_mongodb_connect_url()
        self.mongo_conn = pymongo.MongoClient(mongo_url)

    def _db_session(self, db_name):
        """
        私有方法
        :param db_name: 字符串, 想要创建的 Database 名字
        :return: mongodb 的 数据库 session
        """
        conn = self.mongo_conn
        return conn[db_name]

    def _col_session(self, db_session, col_name):
        """
        私有方法
        :param db_session: mongodb 的 数据库 session
        :param col_name: 字符串，想要创建的 Collection 名字
        :return: mongodb 的 集合 session
        """
        conn = db_session
        return conn[col_name]

    def get_mongo_sess(self, db_name, col_name='default'):
        """
        获取 MongoDB 的文档 session
        :param db_name: 数据库名字
        :param col_name: 集合名字
        :return: 返回 mongo_session 对象
        """
        db_sess = self._db_session(db_name)
        qy_sess = self._col_session(db_sess, col_name)

        return qy_sess
