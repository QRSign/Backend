from flask import Flask
from .CheckIP import CheckIP


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/ip')
def ip():
    if CheckIP().getIp():
        return "true"
    else:
        return "false"


"""if __name__ == '__main__':
    app.run()"""
