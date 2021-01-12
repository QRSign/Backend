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
    enc_password = session.query(User.password).filter(User.mail == mail).first()
    first_name = session.query(User.first_name).filter(User.first_name == mail).first()
    last_name = session.query(User.last_name).filter(User.mail == mail).first()

    user = User(first_name, last_name, mail, password)

    if not enc_password:
        return {'login': "Wrong credential"}, 400
    elif check_password(password, enc_password[0]):
        return user.serialize, 200
    else:
        return {'login': "Wrong credential"}, 400


def add_user(json, session):
    last_name = json['last_name']
    first_name = json['first_name']
    mail = json['mail']
    password = json['password']
    mail_check = session.query(User.mail).filter(User.mail == mail).first()
    if mail_check:
        return {'register': "user already exist"}, 400

    session.add(User(first_name, last_name, mail, password))
    session.commit()

    return {'register': "successful"}, 200


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

    @property
    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'mail': self.mail
        }
