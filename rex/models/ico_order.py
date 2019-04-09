import datetime
from mongokit import Document
from rex import app, db
import validators

__author__ = 'taijoe'


class IcoOrder(Document):
    __collection__ = 'ico'

    structure = {
        'uid':  unicode,
        'user_id': unicode,
        'username': unicode,
        'amount_sva': float,
        'amount_btc' :  float,
        'rate': float,
        'date_added' : datetime.datetime
    }
    use_dot_notation = True

db.register([IcoOrder])