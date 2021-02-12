from flask import jsonify
from sqlalchemy import Column, String, ForeignKey, LargeBinary
from .entity import Entity, Base


def signature_get_method(session, id):
    qrcode = session.query(Signature).filter(Signature.id == id).first()
    return jsonify(qrcode.serialize)


def signature_post_method(json, session):
    nom = json['nom']
    prenom = json['prenom']
    sign = json['signature']
    token = json['token']

    signature = Signature(nom, prenom, sign, token)

    session.add(signature)
    session.commit()
    return jsonify(signature.serialize)


def signature_patch_method(json, session, id):
    nom = json['nom']
    prenom = json['prenom']
    sign = json['signature']
    token = json['token']

    signature = session.query(Signature).get(id)

    signature.nom = nom
    signature.prenom = prenom
    signature.signature = sign
    signature.token = token

    session.commit()

    return jsonify(signature.serialize)


def signature_delete_method(session, id):
    signature = session.query(Signature).get(id)
    session.delete(signature)

    return jsonify(signature.serialize)


def get_signature_by_token(session, token):
    signature = session.query(Signature).get(token)

    return jsonify(signature.serialize)


class Signature(Entity, Base):
    __tablename__ = 'signature'

    nom = Column(String)
    prenom = Column(String)
    signature = Column(LargeBinary)
    token = Column(String, ForeignKey('qrcode.token'))

    def __init__(self, nom, prenom, signature, token):
        Entity.__init__(self)
        self.nom = nom
        self.prenom = prenom
        self.signature = signature
        self.token = token

    @property
    def serialize(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'prenom': self.prenom,
            'signature': self.signature,
            'token': self.token
        }
