from sqlalchemy import Column, String

from .entity import Entity, Base


class User(Entity, Base):
    __tablename__ = 'user'

    name = Column(String)

    def __init__(self, name):
        Entity.__init__(self)
        self.name = name
