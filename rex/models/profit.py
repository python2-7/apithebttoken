import datetime
from mongokit import Document
from rex import app, db
import validators

__author__ = 'taijoe'


class Profit(Document):
    __collection__ = 'profits'

    structure = {
        '500': float
        '1000':  float,
        '3000' : float,
        '5000' : float,
        '10000' : float,
        '30000' : float,
        '50000': float
        '100000':  float,
        '500000' : float,
        '1000000' : float
    }
    use_dot_notation = True

db.register([Profit])