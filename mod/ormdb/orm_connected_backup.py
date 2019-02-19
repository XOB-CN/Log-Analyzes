# -*- coding:utf-8 -*-

from mod.tools import To_MySQL
from sqlalchemy import Column, Integer, String, Text

# 需要继承 ORM 的基类, 这个基类定义在 mod.tools.TO_MySQL 中
class ZipAgent_Summary(To_MySQL.Base):
    __tablename__ = 'zipagent_summary'

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_type = Column(String(32))
    event_status = Column(String(32))
    event_time = Column(String(40))
    event_warn = Column(Text)
    event_error = Column(Text)
    event_diag = Column(Text)

    def __repr__(self):
        return "<ZipAgent_Summary(event_type=%s, event_status=%s, event_time=%s, event_warn=%s, event_error=%s, event_diag=%s)>" %(self.event_type, self.event_status, self.event_time, self.event_warn, self.event_error, self.event_diag)