import datetime
from mongokit import Document
from rex import app, db
import validators

__author__ = 'taijoe'


class Dialing(Document):
    __collection__ = 'dialing'

    structure = {
       
        'customer_id': unicode,
        'username': unicode,
        'package':  float,
        'amount_coin': float,
        'currency': unicode,
        'date_added' : datetime.datetime,
        'status': int
    }
    use_dot_notation = True

db.register([Dialing])