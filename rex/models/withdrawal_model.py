import datetime
from mongokit import Document
from rex import app, db
import validators

__author__ = 'taijoe'


class Withdraw(Document):
    __collection__ = 'withdraw'

    structure = {
        'uid':  unicode,
        'user_id': unicode,
        'username': unicode,
        'amount' :  float,
        'amount_usd' : unicode,
        'status': int,
        'date_added' : datetime.datetime,
        'wallet' : unicode,
        'code_active': unicode,
        'currency': unicode,
        'active_email': int,
        'price' : float
    }
    use_dot_notation = True

db.register([Withdraw])