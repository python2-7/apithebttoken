import datetime
from mongokit import Document
from rex import app, db
import validators

__author__ = 'taijoe'


class Contact(Document):
    __collection__ = 'contact'

    structure = {
        'uid': unicode,
        'username': unicode,
        'name': unicode,
        'address':  unicode,
        'currency': unicode,
        'date_added' : datetime.datetime,
        'status': int,
    }
    use_dot_notation = True

db.register([Contact])