import datetime
from mongokit import Document
from rex import app, db
import validators

__author__ = 'taijoe'


class Withdrawal(Document):
    __collection__ = 'withdrawa'

    structure = {
        'uid':  unicode,
        'user_id': unicode,
        'username': unicode,
        'amount' :  float,
        'amount_usd' :  float,
        'tx':  unicode,
        'status': int,
        'date_added' : datetime.datetime,
        'wallet' : unicode,
        'type': unicode,
        'code_active': unicode,
        'currency': unicode,
        'active_email': int,
        'id_withdraw' : unicode
    }
    use_dot_notation = True

db.register([Withdrawal])