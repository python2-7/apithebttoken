import datetime
from mongokit import Document
from rex import app, db
import validators

__author__ = 'taijoe'


class Notification(Document):
    __collection__ = 'notification'

    structure = {
        'user_id': unicode,
        'uid': unicode,
        'username': unicode,
        'content':  unicode,
        'date_added' : datetime.datetime,
        'status': int,
        'type' : unicode,
        'read' : int
    }
    use_dot_notation = True

db.register([Notification])