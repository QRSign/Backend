from flask import Flask, request, jsonify
from .dao.entities.entity import Session, engine, Base
from .dao.entities.qrcode import Qrcode, qrcode_get_method, qrcode_post_method, qrcode_patch_method, \
    qrcode_delete_method
from .dao.entities.user import get_password, add_user
from datetime import datetime

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

app = Flask(__name__)

session = Session()
Base.metadata.create_all(engine)

connection = 'connection'

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'A_CHANGER'  # Créer une variable d'environnement
jwt = JWTManager(app)

access_token = create_access_token(identity=connection)

@app.route('/login', methods=['POST'])
def login():
    return get_password(request.get_json(), session)

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

@app.route('/register', methods=['POST'])
def register():
    return add_user(request.get_json(), session)


@app.route('/qrcode/<id>', methods=['GET'])
def get_qrcode_by_id(id):
    return qrcode_get_method(request.get_json(), session)


@app.route('/qrcode', methods=['POST'])
def create_qrcode():
    return qrcode_post_method(request.json, session)


@app.route('/qrcode/<id>', methods=['PATCH'])
def update_qrcode_by_id(id):
    return qrcode_patch_method(request.get_json(), session, id)


@app.route('/qrcode/<id>', methods=['DELETE'])
def delete_qrcode_by_id(id):
    return qrcode_delete_method(session, id)