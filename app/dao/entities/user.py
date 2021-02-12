from flask import jsonify
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
    user = session.query(User).filter(User.mail == mail).all()[0]

    print(check_password(password, user.password))

    if not user or not check_password(password, user.password):
        return {'message': "Wrong credential"}, 400
    elif check_password(password, user.password):
        return jsonify(user.serialize), 200


def add_user(json, session):
    last_name = json['last_name']
    first_name = json['first_name']
    mail = json['mail']
    password = json['password']
    mail_check = session.query(User.mail).filter(User.mail == mail).first()
    if mail_check:
        return {'message': "User already exist"}, 400

    user = User(first_name, last_name, mail, password)

    session.add(user)
    session.commit()

    return jsonify(user.serialize), 200


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
