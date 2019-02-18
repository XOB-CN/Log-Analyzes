from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text

Base = declarative_base()

class ZipAgent_Summary():
    __tablename__ = 'zipagent_summary'

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_type = Column(String(32))
    event_status = Column(String(32))
    event_time = Column(String(32))
    event_warn = Column(Text)
    event_error = Column(Text)
    event_diag = Column(Text)

    def __repr__(self):
        return "<ZipAgent_Summary(event_type=%s, event_status=%s, event_time=%s, event_warn=%s, event_error=%s, event_diag=%s)>" %(self.event_type,
                                                                                                                                   self.event_status,
                                                                                                                                   self.event_time,
                                                                                                                                   self.event_warn,
                                                                                                                                   self.event_error,
                                                                                                                                   self.event_diag)