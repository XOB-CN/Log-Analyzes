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

    def add_db(self, db_name):
        """
        :param db_name: 字符串, 想要创建的 Database 名字
        :return: mongodb 的 数据库 session
        """
        conn = self.mongo_conn
        return conn[db_name]

    def add_col(self, db_session, col_name):
        """
        :param db_session: mongodb 的 数据库 session
        :param col_name: 字符串，想要创建的 Collection 名字
        :return: mongodb 的 集合 session
        """
        conn = db_session
        return conn[col_name]

    def get_mongo_docs(self, db_name, col_name):
        db_sess = self.add_db(db_name)
        qy_sess = self.add_col(db_sess, col_name)

        return qy_sess
