import datetime
from mongokit import Document
from rex import app, db
import validators

__author__ = 'taijoe'


class Tree_all(Document):
    __collection__ = 'tree_all'

    use_dot_notation = True

db.register([Tree_all])