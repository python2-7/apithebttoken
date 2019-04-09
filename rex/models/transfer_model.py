import datetime
from mongokit import Document
from rex import app, db
import validators

__author__ = 'taijoe'


class Transfer(Document):
    __collection__ = 'transfer'

    structure = {
        'uid':  unicode,
        'user_id': unicode,
        'username': unicode,
        'amount' :  float,
        'status': int,
        'from' : unicode,
        'to' : unicode,
        'date_added' : datetime.datetime,
        'type' : unicode
    }
    use_dot_notation = True

db.register([Transfer])