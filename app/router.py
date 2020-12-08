from flask import Flask, request
from .dao.entities.entity import Session, engine, Base
from .dao.entities.user import get_password, add_user

app = Flask(__name__)

session = Session()
Base.metadata.create_all(engine)


@app.route('/login')
def login():
    return get_password(request.get_json(), session)


@app.route('/register')
def register():
    return add_user(request.get_json(), session)
