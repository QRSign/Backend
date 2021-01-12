from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from .entity import Entity, Base


class Qrcode(Entity, Base):
    __tablename__ = 'qrcode'

    title = Column(String)
    token = Column(String)
    created_by = Column(Integer, ForeignKey('user.id'))
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    def __init__(self, title, token, created_by, start_time, end_time):
        Entity.__init__(self)
        self.title = title
        self.token = token
        self.created_by = created_by
        self.start_time = start_time
        self.end_time = end_time

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'token': self.token,
            'user': self.created_by,
            'start_time': self.start_time,
            'end_time': self.end_time
        }
