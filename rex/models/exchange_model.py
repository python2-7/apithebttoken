import datetime
from mongokit import Document
from rex import app, db
import validators

__author__ = 'taijoe'


class Exchange(Document):
    __collection__ = 'exchange'

    structure = {
        'uid':  unicode,
        'user_id': unicode,
        'username': unicode,
        'detail':  unicode,
        'amount_form': float,
        'amount_to' :  float,
        'currency_from' :  unicode,
        'currency_to' :  unicode,
        'price_form' : float,
        'price_to':  float,
        'date_added' : datetime.datetime
    }
    use_dot_notation = True

db.register([Exchange])