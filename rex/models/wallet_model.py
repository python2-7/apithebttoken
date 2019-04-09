import datetime
from mongokit import Document
from rex import app, db
import validators

__author__ = 'taijoe'


class Wallet(Document):
    __collection__ = 'wallet'

    structure = {
        'user_id': unicode,
        'uid': unicode,
        'username': unicode,
        'confirmations': int,
        'tx':  unicode,
        'amount': float,
        'type': unicode,
        'date_added' : datetime.datetime,
        'status': int,
        'address': unicode,
        'txt_id' : unicode,
        'amount_usd': float,
        'price' : float,
        'currency' : unicode
    }
    use_dot_notation = True

db.register([Wallet])