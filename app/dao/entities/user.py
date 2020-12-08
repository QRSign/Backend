from sqlalchemy import Column, String, Integer
from .entity import Entity, Base
import hashlib
import uuid


def check_password(raw_password, enc_password):
    salt, key = enc_password.split('$')
    new_key = hashlib.sha256(salt.encode() + raw_password.encode()).hexdigest()

    return key == new_key


def get_password(json, session):
    mail = json['mail']
    password = json['password']
    enc_password = session.query(User.password).filter(User.mail == mail).first()[0]

    if enc_password == "":
        return {'login': "Wrong mail"}
    elif check_password(password, enc_password):
        return {'login': True}
    else:
        return {'login': "Wrong Password"}


def add_user(json, session):
    last_name = json['last_name']
    first_name = json['first_name']
    mail = json['mail']
    password = json['password']
    mail_check = session.query(User.mail).filter(User.mail == mail).first()[0]

    if mail_check != "":
        return {'register': "user already exist"}

    session.add(User(first_name, last_name, mail, password))
    session.commit()

    return {'register': "successful"}


class User(Entity, Base):
    __tablename__ = 'user'

    first_name = Column(String)
    last_name = Column(String)
    mail = Column(String, unique=True)
    password = Column(String)
    role = Column(Integer)

    def __init__(self, first_name, last_name, mail, password):
        Entity.__init__(self)
        self.first_name = first_name
        self.last_name = last_name
        self.mail = mail
        self.set_password(password)
        self.role = 0

    def set_password(self, raw_password):
        salt = uuid.uuid4().hex
        key = hashlib.sha256(salt.encode() + raw_password.encode()).hexdigest()
        self.password = '%s$%s' % (salt, key)
