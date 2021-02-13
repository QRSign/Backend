from flask import Flask, request
from .dao.entities.entity import Session, engine, Base
from .dao.entities.qrcode import qrcode_get_method, qrcode_post_method, qrcode_patch_method, \
    qrcode_delete_method, qrcode_get_method_by_token, qrcodes_get_method
from .dao.entities.signature import signature_get_method, signature_post_method, signature_patch_method, \
    signature_delete_method, get_signature_by_token
from .dao.entities.catho_user import get_password, add_user, get_users_method
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

session = Session()
Base.metadata.create_all(engine)


@app.route('/test')
def test_route():
    return 'test route ok'


@app.route('/users', methods=['GET'])
def get_users():
    return get_users_method(request.get_json(), session)


@app.route('/login', methods=['POST'])
def login():
    return get_password(request.get_json(), session)


@app.route('/register', methods=['POST'])
def register():
    return add_user(request.get_json(), session)


@app.route('/qrcodes', methods=['GET'])
def get_qrcodes():
    return qrcodes_get_method(session)


@app.route('/qrcode/<id>', methods=['GET'])
def get_qrcode_by_id(id):
    return qrcode_get_method(session, id)


@app.route('/qrcode/token/<token>', methods=['GET'])
def get_qrcode_by_token(token):
    return qrcode_get_method_by_token(session, token)


@app.route('/qrcode', methods=['POST'])
def create_qrcode():
    return qrcode_post_method(request.json, session)


@app.route('/qrcode/<id>', methods=['PATCH'])
def update_qrcode_by_id(id):
    return qrcode_patch_method(request.get_json(), session, id)


@app.route('/qrcode/<id>', methods=['DELETE'])
def delete_qrcode_by_id(id):
    return qrcode_delete_method(session, id)


@app.route('/signature/<id>', methods=['GET'])
def get_signature_by_id(id):
    return signature_get_method(request.get_json(), session)


@app.route('/signature', methods=['POST'])
def create_signature():
    return signature_post_method(request.json, session)


@app.route('/signature/<id>', methods=['PATCH'])
def update_signature_by_id(id):
    return signature_patch_method(request.get_json(), session, id)


@app.route('/signature/<id>', methods=['DELETE'])
def delete_signature_by_id(id):
    return signature_delete_method(session, id)


@app.route('/signature/qrcode/<token>', methods=['GET'])
def list_signature_by_token(token):
    return get_signature_by_token(session, token)
