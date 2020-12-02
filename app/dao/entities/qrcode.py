from sqlalchemy import Column, String, Integer, ForeignKey

from .entity import Entity, Base


class Qrcode(Entity, Base):
    __tablename__ = 'qrcode'

    title = Column(String)
    token = Column(String)
    created_by = Column(Integer, ForeignKey('user.id'))

    def __init__(self, title, token, created_by):
        self.title = title
        self.token = token
        self.created_by = created_by
