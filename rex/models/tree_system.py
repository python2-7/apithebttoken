import datetime
from mongokit import Document
from rex import app, db
import validators

__author__ = 'taijoe'


class Support(Document):
    __collection__ = 'tree'

    structure = {
        'customer_id' : unicode,
        'count_left' : unicode,
        'count_right': unicode,
        'json_tree': unicode,
        'username' : unicode
    }
    use_dot_notation = True

db.register([Support])