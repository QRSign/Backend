import secrets

from flask import Flask, render_template
import qrcode

app = Flask(__name__)

@app.route('/')
def hello_world():
    return secrets.token_urlsafe()

@app.route('/qrcode')
def hello():
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data('google.fr')
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save('./static/qrcode.png')
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
