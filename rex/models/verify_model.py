import datetime
from mongokit import Document
from rex import app, db
import validators

__author__ = 'taijoe'


class Verify(Document):
    __collection__ = 'verify'

    structure = {
        'user_id': unicode,
        'uid': unicode,
        'username': unicode,
        'img1': unicode,
        'img2' : unicode,
        'img3': unicode,
        'date_added': datetime.datetime,
        'id_number' : unicode,
        'admin_note': unicode,
        'status' : float
    }
    use_dot_notation = True

db.register([Verify])