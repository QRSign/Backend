from flask import jsonify
from sqlalchemy import Column, String, Integer
from .entity import Entity, Base
import hashlib
import uuid


def check_password(raw_password, enc_password):
    salt, key = enc_password.split('$')
    new_key = hashlib.sha256(salt.encode() + raw_password.encode()).hexdigest()

    return key == new_key


def get_users_method(json, session):
    users = session.query(CathoUser).all()
    if not users:
        return {'error': "Users not found.",
                'message': ""}, 404
    else:
        return jsonify([x.serialize for x in users]), 200


def get_password(json, session):
    mail = json['mail'].lower()
    password = json['password']
    user = session.query(CathoUser).filter(CathoUser.mail == mail).all()

    if not user:
        return {'error': "Wrong credential",
                'message': "L\'adresse mail ou le mot de passe est invalide."}, 400

    user = user[0]

    if not check_password(password, user.password):
        return {'error': "Wrong credential",
                'message': "L\'adresse mail ou le mot de passe est invalide."}, 400
    elif check_password(password, user.password):
        return jsonify(user.serialize), 200


def add_user(json, session):
    last_name = json['last_name']
    first_name = json['first_name']
    mail = json['mail'].lower()
    password = json['password']
    mail_check = session.query(CathoUser.mail).filter(CathoUser.mail == mail).first()
    if mail_check:
        return {'error': "CathoUser already exist",
                'message': "Ce mail a déjà été utilisé."}, 400

    user = CathoUser(first_name, last_name, mail, password)

    session.add(user)
    session.commit()

    return jsonify(user.serialize), 200


class CathoUser(Entity, Base):
    __tablename__ = 'catho_user'

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
