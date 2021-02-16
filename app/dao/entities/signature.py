import pdfkit
import copy
from flask import jsonify, render_template, make_response
from sqlalchemy import Column, String, ForeignKey, LargeBinary
from .catho_user import CathoUser
from .entity import Entity, Base
from . import qrcode


def signatures_get_method(session):
    signature = session.query(Signature).all()
    if not signature:
        return {'error': "QrCode not found.",
                'message': "Token inconnu."}, 404
    else:
        return jsonify([x.serialize for x in signature]), 200


def signature_get_method(session, id):
    signature = session.query(Signature).filter(Signature.id == id).first()
    return jsonify(signature.serialize)


def signature_post_method(json, session):
    nom = json['last_name']
    prenom = json['first_name']
    sign = json['signature'].encode()
    token = json['token']

    signature = Signature(nom, prenom, sign, token)

    session.add(signature)
    session.commit()
    return jsonify(signature.serialize)


def signature_patch_method(json, session, id):
    nom = json['last_name']
    prenom = json['first_name']
    sign = json['signature'].encode()
    token = json['token']

    signature = session.query(Signature).get(id)

    signature.last_name = nom
    signature.first_name = prenom
    signature.signature = sign
    signature.token = token

    session.commit()

    return jsonify(signature.serialize)


def signature_delete_method(session, id):
    signature = session.query(Signature).get(id)
    session.delete(signature)
    session.commit()

    return jsonify(signature.serialize)


def get_signature_by_token(session, token):
    signatures = session.query(Signature).filter(Signature.token == token).all()

    return jsonify([x.serialize for x in signatures])


def get_list_student(session, token):
    informations = copy.deepcopy(session.query(Signature).filter(Signature.token == token).all())
    course = session.query(qrcode.Qrcode).filter(qrcode.Qrcode.token == token).all()[0]
    user = session.query(CathoUser).filter(CathoUser.id == course.created_by).all()[0]
    for info in informations:
        info.signature = info.signature.decode()

    rendered = render_template('list.html', informations=informations, course=course, user=user)
    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    options = {'enable-local-file-access': None}

    pdf_test = pdfkit.from_string(rendered, False, configuration=config, options=options)

    response = make_response(pdf_test)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['content-Disposition'] = 'attachment; filename=list_student.pdf'

    return response


class Signature(Entity, Base):
    __tablename__ = 'signature'

    last_name = Column(String)
    first_name = Column(String)
    signature = Column(LargeBinary)
    token = Column(String, ForeignKey('qrcode.token'), nullable=False)

    def __init__(self, nom, prenom, signature, token):
        Entity.__init__(self)
        self.last_name = nom
        self.first_name = prenom
        self.signature = signature
        self.token = token

    @property
    def serialize(self):
        return {
            'id': self.id,
            'last_name': self.last_name,
            'first_name': self.first_name,
            'signature': self.signature.decode(),
            'token': self.token
        }
