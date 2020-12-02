from .entities.entity import Session, engine, Base
from .entities.qrcode import Qrcode
from .entities.user import User

Base.metadata.create_all(engine)

session = Session()

qrcodes = session.query(Qrcode).all()

if len(qrcodes) == 0:
    user = User("Pierre")
    qrcode = Qrcode("DevOps", "test-token", user.id)
    session.add(qrcode)
    session.add(user)
    session.commit()
    session.close()

    qrcodes = session.query(Qrcode).all()

print('### Qrcodes:')
for qrcode in qrcodes:
    print(f'({qrcode.created_by}) {qrcode.title} - {qrcode.token}')
