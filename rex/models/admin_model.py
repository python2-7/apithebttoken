import datetime
from mongokit import Document
from rex import app, db
import validators

__author__ = 'taijoe'


class Admin(Document):
    __collection__ = 'admins'

    structure = {
        'username':  unicode,
        'email' :  unicode,
        'password': unicode,
        'sum_withdraw': float,
        'sum_invest' : float,
        'status_withdraw' : int
    }
    use_dot_notation = True

db.register([Admin])