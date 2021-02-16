from flask import jsonify
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
import secrets
from datetime import datetime

from sqlalchemy.orm import relationship

from .catho_user import CathoUser
from .entity import Entity, Base
from . import signature


def qrcodes_get_method(session):
    qrcodes = session.query(Qrcode).all()
    if not qrcodes:
        return {'error': "QrCode not found.",
                'message': "Aucun Qrcode disponible."}, 404
    else:
        return jsonify([x.serialize for x in qrcodes]), 200


def qrcode_get_method(session, id):
    qrcode = session.query(Qrcode).filter(Qrcode.id == id).first()
    if not qrcode:
        return {'error': "QrCode not found.",
                'message': "Ce QrCode n'existe pas."}, 404

    return jsonify(qrcode.serialize), 200


def qrcode_get_method_by_token(session, token):
    signatures = session.query(Qrcode).filter(Qrcode.token == token).all()
    if not signatures:
        return {'error': "Unknown token",
                'message': "Token inconnu."}, 400
    else:
        return jsonify(signatures[0].serialize), 200


def qrcode_post_method(json, session):
    title = json['title']
    token = secrets.token_hex(4)
    user_id = json['user']

    if type(user_id) != int:
        return {'error': 'Id is not an integer',
                'message': "Le formulaire n\'a pas été correctement rempli."}, 400

    try:
        start_time = datetime.strptime(json['start_time'], "%Y-%m-%d %H:%M")
        end_time = datetime.strptime(json['end_time'], "%Y-%m-%d %H:%M")
    except Exception as e:
        print(e)
        return {'error': 'Wrong date format',
                'message': "Format de la date incorrect."}, 400

    user = session.query(CathoUser).get(user_id)

    if not user:
        return {'error': 'User not found.',
                'message': "Le formulaire n\'a pas été correctement rempli."}, 404

    qrcode = Qrcode(title, token, user_id, start_time, end_time)

    session.add(qrcode)
    session.commit()
    return jsonify(qrcode.serialize), 201


def qrcode_patch_method(json, session, id):
    title = json['title']
    user = json['user']
    start_time = datetime.strptime(json['start_time'], "%Y-%m-%d %H:%M")
    end_time = datetime.strptime(json['end_time'], "%Y-%m-%d %H:%M")

    qrcode = session.query(Qrcode).get(id)

    if not qrcode:
        return {'error': "QrCode not found.",
                'message': ""}, 404

    qrcode.title = title
    qrcode.user = user
    qrcode.start_time = start_time
    qrcode.end_time = end_time

    session.commit()

    return jsonify(qrcode.serialize), 200


def qrcode_delete_method(session, id):
    qrcode = session.query(Qrcode).get(id)
    signatures = session.query(signature.Signature).filter(signature.Signature.token == qrcode.token).all()
    for sign in signatures:
        session.delete(sign)

    session.delete(qrcode)

    return jsonify(qrcode.serialize)


class Qrcode(Entity, Base):
    __tablename__ = 'qrcode'

    title = Column(String)
    token = Column(String, unique=True, nullable=False)
    created_by_id = Column(Integer, ForeignKey('catho_user.id'))
    created_by = relationship("CathoUser")
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    def __init__(self, title, token, created_by_id, start_time, end_time):
        Entity.__init__(self)
        self.title = title
        self.token = token
        self.created_by_id = created_by_id
        self.start_time = start_time
        self.end_time = end_time

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'token': self.token,
            'user': self.created_by.serialize,
            'start_time': self.start_time,
            'end_time': self.end_time
        }
