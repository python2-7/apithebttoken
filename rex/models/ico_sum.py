import datetime
from mongokit import Document
from rex import app, db
import validators

__author__ = 'taijoe'


class Icosum(Document):
    __collection__ = 'icosum'

    use_dot_notation = True

db.register([Icosum])