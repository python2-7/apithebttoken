import datetime
from mongokit import Document
from rex import app, db
import validators

__author__ = 'taijoe'


class WithdrawalPayment(Document):
    __collection__ = 'withdrawal_payment'

    structure = {
        'uid':  unicode,
        'detail':  unicode,
        'amount_sub' :  float,
        'amount_rest' : float,
        'amount_btc' : float,
        'txtid':  unicode,
        'status': float,
        'date_added' : datetime.datetime,
        'wallet' : unicode,
        'withdraw_id': unicode,
        'method_payment': int
    }
    use_dot_notation = True

db.register([WithdrawalPayment])