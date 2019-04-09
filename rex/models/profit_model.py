import datetime
from mongokit import Document
from rex import app, db
import validators

__author__ = 'taijoe'


class Profit(Document):
    __collection__ = 'profit'

    structure = {
        'date_added' : datetime.datetime,
        'percent' : float,
        'status': int
    }
    use_dot_notation = True

db.register([Profit])