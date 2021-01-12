from flask import Flask, request, jsonify
from .dao.entities.entity import Session, engine, Base
from .dao.entities.qrcode import Qrcode
from .dao.entities.user import get_password, add_user
import secrets
from datetime import datetime

app = Flask(__name__)

session = Session()
Base.metadata.create_all(engine)


@app.route('/login')
def login():
    return get_password(request.get_json(), session)


@app.route('/register')
def register():
    return add_user(request.get_json(), session)


@app.route('/qrcode', methods=['POST'])
def create_qrcode():
    json_obj = request.get_json()
    title = json_obj['title']
    token = secrets.token_hex(4)
    user = json_obj['user']
    start_time = datetime.strptime(json_obj['start_time'], "%Y-%m-%d %H:%M")
    end_time = datetime.strptime(json_obj['start_time'], "%Y-%m-%d %H:%M")

    qrcode = Qrcode(title, token, user, start_time, end_time)

    session.add(qrcode)
    session.commit()
    return jsonify(qrcode.serialize)


@app.route('/qrcode/<id>', methods=['GET'])
def get_qrcode_by_id(id):
    spot = session.query(Qrcode).filter(Qrcode.id == id).first()

    return jsonify(spot.serialize)


@app.route('/qrcode/<id>', methods=['PATCH'])
def update_qrcode_by_id(id):
    json_obj = request.get_json()
    title = json_obj['title']
    user = json_obj['user']
    start_time = datetime.strptime(json_obj['start_time'], "%Y-%m-%d %H:%M")
    end_time = datetime.strptime(json_obj['end_time'], "%Y-%m-%d %H:%M")

    qrcode = session.query(Qrcode).get(id)

    qrcode.title = title
    qrcode.user = user
    qrcode.start_time = start_time
    qrcode.end_time = end_time

    session.commit()

    return jsonify(qrcode.serialize)


@app.route('/qrcode/<id>', methods=['DELETE'])
def delete_qrcode_by_id(id):
    spot = session.query(Qrcode).get(id)
    session.delete(spot)

    return jsonify(spot.serialize)