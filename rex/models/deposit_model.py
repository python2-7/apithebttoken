import datetime
from mongokit import Document
from rex import app, db
import validators

__author__ = 'taijoe'


class Deposit(Document):
    __collection__ = 'deposit'

    structure = {
        'confirmations': int,
        'user_id': unicode,
        'uid': unicode,
        'username': unicode,
        'tx':  unicode,
        'amount': float,
        'type': unicode,
        'date_added' : datetime.datetime,
        'status': int,
        'address': unicode,
        'txn_id' : unicode,
        'amount_usd': float,
        'price' : float
    }
    use_dot_notation = True

db.register([Deposit])