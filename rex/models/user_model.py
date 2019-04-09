import datetime
from mongokit import Document
from rex import app, db
import validators
from bson.objectid import ObjectId
__author__ = 'taijoe'


class User(Document):
    __collection__ = 'users'

    structure = {
        'customer_id' : unicode,
        'email': unicode,
        'code_active': unicode,
        'username': unicode,
        'password': unicode,
        'creation': datetime.datetime,
        'p_binary' : unicode,
        'left' : unicode,
        'right' : unicode,
        'telephone' : float,
        'league' : int,
        'p_node' : unicode,
        'password_transaction' : unicode,
        'level' : int,
        'password_custom' : unicode,
        'total_pd_left' : float,
        'total_pd_right' : float,
        'total_amount_left' : float,
        'total_amount_right': float,
        'm_wallet' : float,
        'r_wallet' : float,
        's_wallet' : float,
        'd_wallet' : float,
        'l_wallet' : float,
        'ss_wallet' : float,
        'sf_wallet' : float,
        
        'total_earn' : float,
        
        'investment': float,
        'total_node' : float,
        'status' : int,
        'balance' : {
            'bitcoin' : {
                'cryptoaddress' : unicode,
                'available' : float
            },
            'ethereum' : {
                'cryptoaddress' : unicode,
                'available' : float
            },
            'bitcoincash' : {
                'cryptoaddress' : unicode,
                'available' : float
            },
            'dogecoin' : {
                'cryptoaddress' : unicode,
                'available' : float
            },
            'litecoin' : {
                'cryptoaddress' : unicode,
                'available' : float
            },
            'dash' : {
                'cryptoaddress' : unicode,
                'available' : float
            },
            'ripple' : {
                'cryptoaddress' : unicode,
                'available' : float
            },
            'eos' : {
                'cryptoaddress' : unicode,
                'available' : float
            },
            'tether' : {
                'cryptoaddress' : unicode,
                'available' : float
            },
            'coin' : {
                'cryptoaddress' : unicode,
                'available' : float
            }
        },
        'security' : {
            'code_forgot' : unicode,
            'email' : {
                'code' : unicode,
                'status' : int
            },
            'authenticator' : {
                'code' : unicode,
                'status' : int
            },
            'withdraw' : {
                'code' : unicode,
                'status' : int
            },
            'exchange' : {
                'code' : unicode,
                'status' : int
            },
            'lock_account' : {
                'code' : unicode,
                'status' : int
            },
            'login' : {
                'code' : unicode,
                'status' : int
            },
            'fingerprint' :  {
                'code' : unicode,
                'status' : int
            },
            'count_send_mail' : int
        },
        'personal_info': {
            'firstname' : unicode,
            'lastname' : unicode,
            'date_birthday' :unicode,
            'address' :unicode,
            'postalcode' : unicode,
            'city' : unicode,
            'country' : unicode,
            'img_passport_fontside' : unicode,
            'img_passport_backside' : unicode,
            'img_address' : unicode,
            'img_profile' : unicode,
            'country' :  unicode
        }
    }
    validators = {
        'email': validators.max_length(120)
    }
    default_values = {
        'creation': datetime.datetime.utcnow(),
        'm_wallet' : 0,
        'r_wallet' : 0,
        's_wallet' : 0,
        
        'total_earn' : 0,
        'total_pd_left' : 0,
        'total_pd_right' : 0,
        'total_amount_left' : 0,
        'total_amount_right' : 0,
        'level' : 0,
        'status' : 0,
        'left' : '',
        'right' : '',
        'p_binary' : '',
        
        'investment' : 0,
        
        'total_node' : 0,
        

        }
    use_dot_notation = True

    def __repr__(self):
        return '<User %r>' % self.name

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self._id

    def get_role(self):
        return self.role

    def get_user_home(self):
        role = db['roles'].find_one({'_id': self.get_role()})
        return role['home_page']


db.register([User])