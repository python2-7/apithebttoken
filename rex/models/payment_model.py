import datetime
from mongokit import Document
from rex import app, db
import validators

__author__ = 'taijoe'


class Payment(Document):
    __collection__ = 'payment'

    structure = {
        'uid' : unicode,
        'user_id': unicode,
        'username' : unicode,
        'amount_usd' : float,
        'amount' : float,
        'status' : int,
        'date_added' : datetime.datetime,
        'address' : unicode,
        'currency' : unicode,
        'types' : unicode
    }
    default_values = {
        'date_added': datetime.datetime.utcnow()
        }
    use_dot_notation = True

db.register([Payment])