from flask import Flask, request, jsonify
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
import secrets
from datetime import datetime
from .entity import Entity, Base


def qrcode_get_method(session, id):
    spot = session.query(Qrcode).filter(Qrcode.id == id).first()
    return jsonify(spot.serialize)


def qrcode_post_method(json, session):
    title = json['title']
    token = secrets.token_hex(4)
    user = json['user']
    start_time = datetime.strptime(json['start_time'], "%Y-%m-%d %H:%M")
    end_time = datetime.strptime(json['end_time'], "%Y-%m-%d %H:%M")

    qrcode = Qrcode(title, token, user, start_time, end_time)

    session.add(qrcode)
    session.commit()
    return jsonify(qrcode.serialize)


def qrcode_patch_method(json, session, id):
    title = json['title']
    user = json['user']
    start_time = datetime.strptime(json['start_time'], "%Y-%m-%d %H:%M")
    end_time = datetime.strptime(json['end_time'], "%Y-%m-%d %H:%M")

    qrcode = session.query(Qrcode).get(id)

    qrcode.title = title
    qrcode.user = user
    qrcode.start_time = start_time
    qrcode.end_time = end_time

    session.commit()

    return jsonify(qrcode.serialize)


def qrcode_delete_method(session, id):
    spot = session.query(Qrcode).get(id)
    session.delete(spot)

    return jsonify(spot.serialize)


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
