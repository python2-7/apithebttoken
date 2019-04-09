import datetime
from mongokit import Document
from rex import app, db
import validators

__author__ = 'taijoe'


class Support(Document):
    __collection__ = 'support'

    structure = {
        'date_added' : datetime.datetime,
        'subject' : unicode,
        'message': unicode,
        'user_id': unicode,
        'username' : unicode,
        'reply': [],
        'status': int
    }
    use_dot_notation = True

db.register([Support])