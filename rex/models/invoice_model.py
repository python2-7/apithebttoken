import datetime
from mongokit import Document
from rex import app, db
import validators

__author__ = 'taijoe'


class Invoice(Document):
    __collection__ = 'invoice'

    structure = {
        'uid' : unicode,
        'username' : unicode,
        'amount' : float,
        'invoid_id' : unicode,
        'serect' : unicode,
        'txt' : unicode,
        'callback' : unicode,
        'input_wallet' : unicode,
        'investment_id' : unicode,
        'confirmations' : int,
        'bitcoin' : unicode,
        'my_address' : unicode,
        'fee_percent': unicode,
        'type': int
    }
    default_values = {
        'confirmations' : 0
        }
    use_dot_notation = True

db.register([Invoice])