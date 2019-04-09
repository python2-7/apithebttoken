import datetime
from mongokit import Document
from rex import app, db
import validators

__author__ = 'taijoe'


class Usva(Document):
    __collection__ = 'usva'

    use_dot_notation = True

db.register([Usva])