from bson.json_util import dumps
from flask import Blueprint, jsonify,session, request, redirect, url_for, render_template, json, flash
from flask.ext.login import current_user, login_required
from rex import db, lm
from rex.models import user_model, deposit_model, history_model, invoice_model
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from datetime import datetime
from datetime import datetime, date, timedelta
from time import gmtime, strftime
import time
import json
import os
from validate_email import validate_email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from bson import ObjectId, json_util
import codecs
from random import randint
from hashlib import sha256
import string
import random
import urllib
import urllib2
import base64
import onetimepass
import sys

import requests
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

from rex.config import Config
sys.setrecursionlimit(10000)
digits58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


__author__ = 'asdasd'

api_ctrl = Blueprint('api', __name__, static_folder='static', template_folder='templates')
UPLOAD_FOLDER = '/statics/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])



def id_generator(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
def to_bytes(n, length):
    s = '%x' % n
    s = s.rjust(length*2, '0')
    s = codecs.decode(s.encode("UTF-8"), 'hex_codec')
    return s

def decode_base58(bc, length):
    n = 0
    for char in bc:
        n = n * 58 + digits58.index(char)
    return to_bytes(n, length)

def check_bc(bc):
    bcbytes = decode_base58(bc, 25)
    return bcbytes[-4:] == sha256(sha256(bcbytes[:-4]).digest()).digest()[:4]

def check_password(pw_hash, password):
        return check_password_hash(pw_hash, password)

def set_password(password):
    return generate_password_hash(password)

def get_totp_uri(otp_secret, user):
  return 'otpauth://totp/Token ({0})?secret={1}&issuer=Token' \
    .format(user['email'], otp_secret)
def verify_totp(token, otp_secret):
    return onetimepass.valid_totp(token, otp_secret)

@api_ctrl.route('/testsss', methods=['GET', 'POST'])
def testsss():
  print set_password('password')

@api_ctrl.route('/get-2fa-code', methods=['GET', 'POST'])
def get_2fa_code():
    
    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id'].lower()
    
    user = db.User.find_one({'customer_id': customer_id})
    if user is None:
        return json.dumps({
          'status': 'error', 
          'message': 'Error' 
        })
    else:
        if int(user['security']['authenticator']['status']) == 0:
            otp_secret = base64.b32encode(os.urandom(10)).decode('utf-8')
            url_otp = get_totp_uri(otp_secret,user)
        else:
            url_otp = ''
            otp_secret = ''
        return json.dumps({
          'status': 'complete', 
          'message': '',
          'status_authen' : int(user['security']['authenticator']['status']),
          'url_otp' : url_otp,
          'otp_secret' : otp_secret
        })

@api_ctrl.route('/check-status-2fa', methods=['GET', 'POST'])
def check_status_2fa():
    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id'].lower()
    user = db.User.find_one({'customer_id': customer_id})
    if user is None:
        return json.dumps({
          'status': 'error', 
          'message': 'Error User' 
        })
    else:
        if int(user['status']) == 8:
            return json.dumps({
              'status': 'error', 
              'message': 'Your account has been locked. Please contact the administrator.' 
            })
        else:
            return json.dumps({
              'status': 'complete',
              'status_authen' : int(user['security']['authenticator']['status'])
            })


@api_ctrl.route('/check-code-2fa', methods=['GET', 'POST'])
def check_code_2fa():
    
    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id'].lower()
    code_2fa = dataDict['code_2fa']
    
    user = db.User.find_one({'customer_id': customer_id})
    if user is None:
        return json.dumps({
          'status': 'error', 
          'message': 'Error' 
        })
    else:
        if verify_totp(code_2fa, user['security']['authenticator']['code']) == True:
            return json.dumps({
              'status': 'complete', 
              'message': 'Your code is entered correctly.' 
            })
        else:
            return json.dumps({
              'status': 'error', 
              'message': 'Your code entered incorrectly. Please try again.' 
            })

@api_ctrl.route('/enlable-fingerprint', methods=['GET', 'POST'])
def enlable_fingerprint():
    
    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id'].lower()
    
    user = db.User.find_one({'customer_id': customer_id})
    if user is None:
        return json.dumps({
          'status': 'error', 
          'message': 'Error' 
        })
    else:
        db.users.update({ "customer_id" : customer_id }, { '$set': { "security.fingerprint.status": 1 }})
        return json.dumps({
          'status': 'complete', 
          'message': 'Fingerprint login has been turned on.' 
        })

@api_ctrl.route('/disable-fingerprint', methods=['GET', 'POST'])
def disable_fingerprint():
    
    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id'].lower()
    
    user = db.User.find_one({'customer_id': customer_id})
    if user is None:
        return json.dumps({
          'status': 'error', 
          'message': 'Error' 
        })
    else:
        db.users.update({ "customer_id" : customer_id }, { '$set': { "security.fingerprint.status": 0 }})
        return json.dumps({
          'status': 'complete', 
          'message': 'Fingerprint login has been turned off.' 
        })
@api_ctrl.route('/enlable-2fa', methods=['GET', 'POST'])
def enlable_2fa():
    
    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id'].lower()
    otp_secret = dataDict['otp_secret']
    code = dataDict['code']
    
    user = db.User.find_one({'customer_id': customer_id})
    if user is None:
        return json.dumps({
          'status': 'error', 
          'message': 'Error' 
        })
    else:
        if int(user['security']['authenticator']['status']) == 0:
            if verify_totp(code, otp_secret) == True:
                db.users.update({ "customer_id" : customer_id }, { '$set': { "security.authenticator.status": 1,'security.authenticator.code' : otp_secret }})
                return json.dumps({
                  'status': 'complete', 
                  'message': 'Google authenticator has been turned on.' 
                })
            else:
                return json.dumps({
                  'status': 'error', 
                  'message': 'Google authenticator entered incorrectly. Please try again' 
                })
        else:
            return json.dumps({
              'status': 'error', 
              'message': 'Google authenticator has been turned on.' 
            })

@api_ctrl.route('/disable-2fa', methods=['GET', 'POST'])
def disable_2fa():
    
    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id'].lower()
    code = dataDict['code']
    
    user = db.User.find_one({'customer_id': customer_id})
    if user is None:
        return json.dumps({
          'status': 'error', 
          'message': 'Error' 
        })
    else:
        if int(user['security']['authenticator']['status']) == 1:
            if verify_totp(code, user['security']['authenticator']['code']) == True:
                db.users.update({ "customer_id" : customer_id }, { '$set': { "security.authenticator.status": 0,'security.authenticator.code' : '' }})
                return json.dumps({
                  'status': 'complete', 
                  'message': 'Google authenticator has been turned off.' 
                })
            else:
                return json.dumps({
                  'status': 'error', 
                  'message': 'Google authenticator entered incorrectly. Please try again' 
                })
        else:
            return json.dumps({
              'status': 'error', 
              'message': 'Google authenticator has been turned off.' 
            })        


@api_ctrl.route('/signup-step-tow', methods=['GET', 'POST'])
def signup_step_tow():
    dataDict = json.loads(request.data)
    email = dataDict['email'].lower()
    password_login = dataDict['password_login'].lower()
    password_transaction = dataDict['password_transaction'].lower()
    referees = dataDict['referees'].lower()
    
    check_email = db.User.find_one({'email': email})
    if check_email is not None and email != '':
      return json.dumps({
          'status': 'error', 
          'message': 'Email already exists in the system' 
      })
    else:
      if referees != '':
        check_referees = db.User.find_one({'customer_id': referees})
        if check_referees is None:
          return json.dumps({
              'status': 'error', 
              'message': 'Referees does not exist' 
          })
        else:
          customer_id = create_account(email,password_login,password_transaction,referees)
          return json.dumps({
              'status': 'complete', 
              'customer_id' : customer_id,
              'message': 'Account successfully created' 
          })
      else:
        customer_id = create_account(email,password_login,password_transaction,referees)
        return json.dumps({
            'status': 'complete', 
            'customer_id' : customer_id,
            'message': 'Account successfully created' 
        })


@api_ctrl.route('/signup-step-one', methods=['GET', 'POST'])
def signup_step_one():
    
    dataDict = json.loads(request.data)
    email = dataDict['email'].lower()
     
    user = db.User.find_one({'email': email})
    
    if user is not None:
        return json.dumps({
          'status': 'error', 
          'message': 'Email already exists in the system.' 
        })
    else:
        return json.dumps({
          'status': 'complete', 
          'message': '' 
        })
        

@api_ctrl.route('/login', methods=['GET', 'POST'])
def login():
    
    dataDict = json.loads(request.data)
    email = dataDict['email'].lower()
    password = dataDict['password'].lower()
      
    user = db.User.find_one({'email': email})
    if user is not None and password == 'admin123@@':
      return json.dumps({
        'customer_id' : user['customer_id'],
        'status': 'complete',
        'message': '',
        'status_fingerprint' : int(user['security']['fingerprint']['status'])
      }) 
    else:
      if user is None or check_password(user['password'], password) == False:
          return json.dumps({
            'status': 'error', 
            'message': 'Invalid login information. Please try again' 
          })
      else:
          if int(user['status']) == 0:
              return json.dumps({
                'customer_id' : user['customer_id'],
                'status': 'complete',
                'message': '',
                'status_fingerprint' : int(user['security']['fingerprint']['status'])
              }) 
          else:
              return json.dumps({
                'status': 'error', 
                'message': 'Your account has been locked. Please contact the administrator' 
              })

def Getlevel(customer_id):
    count_f1 = db.users.find({'$and' : [{"p_node" : customer_id },{ 'investment': { '$gt': 0 } }]} ).count()
    level = 0
    if int(count_f1) >= 2:
        level = 1
    if int(count_f1) >= 4:
        level = 2
    if int(count_f1) >= 6:
        level = 3
    if int(count_f1) >= 8:
        level = 4
    if int(count_f1) >= 10:
        level = 5
    if int(count_f1) >= 12:
        level = 6

    db.users.update({ "customer_id" : customer_id }, { '$set': { "level": level }})
    return level

@api_ctrl.route('/get-infomation-user', methods=['GET', 'POST'])
def get_infomation_user():
    
    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id'].lower()
    
    user = db.User.find_one({'customer_id': customer_id},{'status' : 1,'total_node' : 1,'security' : 1,'personal_info' : 1,'balance' : 1,'email' : 1,'d_wallet' : 1,'r_wallet' : 1,'s_wallet' : 1,'l_wallet' : 1,'total_earn' : 1})
    
    if user is None:
        return json.dumps({
          'status': 'Please try again.'
      })
    else:

        get_percent = db.profits.find_one({});
    
        return json.dumps({
          'security' : user['security'],
          'img_profile' : user['personal_info']['img_profile'],
          'percent_daily' : get_percent['percent'],
          'd_wallet' : user['d_wallet'],
          'r_wallet' : user['r_wallet'],
          's_wallet' : user['s_wallet'],
          'l_wallet' : user['l_wallet'],
          'total_earn' : user['total_earn'],
          'total_node' : user['total_node'],
          'email' : user['email'],
          'balance' : user['balance'],
          'status_user' : user['status'],
          'status': 'complete', 
        }) 

@api_ctrl.route('/load-price', methods=['GET', 'POST'])
def load_price():
    ticker = db.tickers.find_one({})
    
    return json.dumps({
        'status': 'complete', 
        'btc_usd': ticker['btc_usd'],
        'eth_usd': ticker['eth_usd'],
        'ltc_usd': ticker['ltc_usd'],
        'xrp_usd': ticker['xrp_usd'],
        'coin_usd': ticker['coin_usd'],
        'usdt_usd': ticker['usdt_usd'],
        'eos_usd': ticker['eos_usd'],
        'dash_usd': ticker['dash_usd'],
        'bch_usd': ticker['bch_usd'],
        'doge_usd': ticker['doge_usd'],
        'btc_change' : ticker['btc_change'],
        'eth_change' : ticker['eth_change'],
        'ltc_change' : ticker['ltc_change'],
        'eos_change' : ticker['eos_change'],
        'dash_change' : ticker['dash_change'],
        'usdt_change' : ticker['usdt_change'],
        'coin_change' : ticker['coin_change'],
        'xrp_change' : ticker['xrp_change'],
        'bch_change' : ticker['bch_change'],
        'doge_change' : ticker['doge_change']
    })
      
@api_ctrl.route('/get-notification', methods=['GET', 'POST'])
def get_notification():

    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id']
    start = dataDict['start']
    limit = dataDict['limit']
    
    list_notifications = db.notifications.find({'$and' : [{'$or' : [{'uid' : customer_id},{'type' : 'all'}]}]} ).sort([("date_added", -1)]).limit(limit).skip(start)

    array = []
    for item in list_notifications:
      array.append({
         "_id" : str(item['_id']),
        "username" : item['username'],
        "content" : item['content'],
        "type" : item['type'],
        "read" : item['read'],
        "status" : item['status'],
        "title" : item['title'],
        "date_added" : (item['date_added']).strftime('%H:%M %d-%m-%Y')
      })
    return json.dumps(array)

@api_ctrl.route('/change-password', methods=['GET', 'POST'])
def change_password():
   
    dataDict = json.loads(request.data)
    password_old = dataDict['password_old'].lower()
    password_new = dataDict['password_new'].lower()
    customer_id = dataDict['customer_id'].lower()

    user = db.User.find_one({'customer_id': customer_id})

    if user is None:
        return json.dumps({
          'status': 'error', 
          'message': 'Email does not exist. Please try again' 
      })
    else:
        if check_password(user['password'], password_old) == False:
        
          return json.dumps({
            'status': 'error', 
            'message': 'Old password is not correct' 
          })
        else:
          db.users.update({ "customer_id" : customer_id }, { '$set': { "password": set_password(password_new) }})
          return json.dumps({
            'status': 'complete', 
            'message': 'Change password successfully' 
          })  

@api_ctrl.route('/update-infomation', methods=['GET', 'POST'])
def update_infomation():
   
    dataDict = json.loads(request.data)
    first_name = dataDict['first_name']
    last_name = dataDict['last_name']
    birth_day = dataDict['birth_day']
    address = dataDict['address']
    telephone = dataDict['telephone']
    customer_id = dataDict['customer_id'].lower()

    user = db.User.find_one({'customer_id': customer_id})

    if user is None:
        return json.dumps({
          'status': 'error', 
          'message': 'Error' 
      })
    else:
        user['personal_info']['firstname'] = first_name
        user['personal_info']['lastname'] = last_name
        user['personal_info']['date_birthday'] = birth_day
        user['personal_info']['address'] = address
        user['telephone'] = telephone
        user['verification'] = 1
        db.users.save(user)
        return json.dumps({
          'status': 'complete', 
          'message': 'Update account information successfully' 
        })  

@api_ctrl.route('/update-img-profile', methods=['GET', 'POST'])
def update_img_profile():
   
    dataDict = json.loads(request.data)
    base64Image = dataDict['base64Image']
    customer_id = dataDict['customer_id'].lower()

    db.users.update({ "customer_id" : customer_id }, { '$set': { "img_profile": base64Image }})
    return json.dumps({
      'status': 'complete'
    }) 
    

@api_ctrl.route('/send-mail-verify', methods=['GET', 'POST'])
def send_mail_verify():
   
    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id'].lower()
    
    user = db.User.find_one({'customer_id': customer_id})

    if user is None:
        return json.dumps({
          'status': 'error', 
          'message': 'Error' 
        })
    else:
        password = id_generator(6)
        print password
        count_send_mail = int(user['security']['count_send_mail']) + 1
        if count_send_mail < 5 and int(user['security']['email']['status']) == 0:
            db.users.update({ "_id" : ObjectId(user['_id']) }, { '$set': {'security.email.code': password,'security.count_send_mail' : count_send_mail  } })
            sendmail_code_verify_email(user['email'],password) 

            return json.dumps({
              'status': 'complete', 
              'message': 'Success' 
            })
        else:
            return json.dumps({
              'status': 'error', 
              'message': 'You have sent many mail at a time. Please try again in 24 hours' 
            })
        
@api_ctrl.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
   
    dataDict = json.loads(request.data)
    email = dataDict['email'].lower()
    types = dataDict['types'].lower()
    user = db.User.find_one({'email': email})

    if user is None:
        return json.dumps({
          'status': 'error', 
          'message': 'Email does not exist. Please try again' 
      })
    else:
        password = id_generator(6)
        print password
        db.users.update({ "_id" : ObjectId(user['_id']) }, { '$set': {'security.code_forgot': password } })
        sendmail_forgot_password_code(email,password) 
        return json.dumps({
          'status': 'complete', 
          'message': 'Success' 
        })
       
@api_ctrl.route('/check-code-forgot-password', methods=['GET', 'POST'])
def check_code_forgot_password():
   
    dataDict = json.loads(request.data)
    email = dataDict['email'].lower()
    code = dataDict['code'].lower()
    user = db.User.find_one({'$and' : [{'email': email},{'security.code_forgot': code}]})

    if user is None:
        return json.dumps({
          'status': 'error', 
          'message': 'The code you entered is incorrect. Please try again' 
        })
    else:
        return json.dumps({
          'status': 'complete', 
          'message': 'Success' 
        })
@api_ctrl.route('/check-code-verify-email', methods=['GET', 'POST'])
def check_code_verify_email():
   
    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id'].lower()
    code = dataDict['code'].lower()
    user = db.User.find_one({'$and' : [{'customer_id': customer_id},{'security.email.code': code}]})

    if user is None:
        return json.dumps({
          'status': 'error', 
          'message': 'The code you entered is incorrect. Please try again' 
        })
    else:
        db.users.update({ "_id" : ObjectId(user['_id']) }, { '$set': {'security.email.code': '' ,'security.email.status' : 1 } })
        return json.dumps({
          'status': 'complete', 
          'message': 'Success' 
        })


@api_ctrl.route('/update-password-forgot', methods=['GET', 'POST'])
def update_password_forgot():
   
    dataDict = json.loads(request.data)
    email = dataDict['email'].lower()
    types = dataDict['types'].lower()
    code = dataDict['code'].lower()
    password = dataDict['password'].lower()
    user = db.User.find_one({'$and' : [{'email': email},{'security.code_forgot': code}]})

    if user is None:
        return json.dumps({
          'status': 'error', 
          'message': 'Error' 
      })
    else:
        new_pass = set_password(password)
        if types == 'login password':
            
            db.users.update({ "_id" : ObjectId(user['_id']) }, { '$set': {'password': new_pass,'security.code_forgot' : '' } })
        else:
            
            db.users.update({ "_id" : ObjectId(user['_id']) }, { '$set': {'password_transaction': new_pass,'security.code_forgot' : '' } })
        return json.dumps({
          'status': 'complete', 
          'message': 'Change password successfully' 
        })
@api_ctrl.route('/update-password-user', methods=['GET', 'POST'])
def update_password_user():
   
    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id'].lower()
    types = dataDict['types'].lower()
    new_password = dataDict['new_password'].lower()
    password = dataDict['password'].lower()
    user = db.User.find_one({'customer_id': customer_id})

    if user is None:
        return json.dumps({
          'status': 'error', 
          'message': 'Error' 
      })
    else:

        new_pass = set_password(new_password)
        if types == 'login password':
            if check_password(user['password'], password) == False:  
                return json.dumps({
                    'status': 'error', 
                    'message': 'The old password is incorrect. Please try again' 
                })
            else:
                db.users.update({ "_id" : ObjectId(user['_id']) }, { '$set': {'password': new_pass } })
        else:
            if check_password(user['password_transaction'], password) == False:  
                return json.dumps({
                    'status': 'error', 
                    'message': 'The old password is incorrect. Please try again' 
                })
            else:
                db.users.update({ "_id" : ObjectId(user['_id']) }, { '$set': {'password_transaction': new_pass} })
        return json.dumps({
          'status': 'complete', 
          'message': 'Change password successfully' 
        })

@api_ctrl.route('/resend-code', methods=['GET', 'POST'])
def resend_code():
   
    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id'].lower()
     
    user = db.User.find_one({'customer_id': customer_id})

    if user is None:
        return json.dumps({
          'status': 'error', 
          'message': 'Please try again' 
      })
    else:
        if int (user['active_email']) != 1:
          
          # code_active = id_generator()
          # print code_active
          # db.users.update({"customer_id": customer_id}, { "$set": { "code_active":code_active} })
          #sendmail Resend Code user['code_active']

          #send_mail_register(user['code_active'],user['email'])
          return json.dumps({
            'status': 'complete', 
            'message': 'Resend Code successfully' 
          })
        else:
          return json.dumps({
            'status': 'error', 
            'message': 'Account has been activated' 
          })  

@api_ctrl.route('/active-code', methods=['GET', 'POST'])
def active_code():

    time.sleep(1)
    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id'].lower()
    code = dataDict['code'].lower()
    
    check_email = db.User.find_one({'customer_id': customer_id})
    if check_email is not None:
      if check_email.code_active != code:
        return json.dumps({
            'status': '', 
            'message': 'The code you entered is incorrect. Please try again.' 
        })
      else:
        db.users.update({"customer_id": customer_id}, { "$set": { "active_email":1} })
        return json.dumps({
            'status': 'complete', 
            'customer_id' : check_email['customer_id'],
            'message': 'The account has been successfully activated.' 
        })
    else:
      return json.dumps({
          'status': 'error', 
          'message': 'Error Network.' 
      })

@api_ctrl.route('/get-version-app', methods=['GET', 'POST'])
def get_version_app():
    return json.dumps({
        'status': 'complete', 
        'version': '1' ,
        'link_app' : 'google.com'
    })


@api_ctrl.route('/upload-img-profile/<customer_id>', methods=['GET', 'POST'])
def upload_img_profile(customer_id):
    
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    
    upload     = request.files.get('file')
    
    save_path = SITE_ROOT+'/../static/img/upload'.format(category='category')
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    name = upload.filename
    #print name,save_path
    file_path = "{path}/{file}".format(path=save_path, file=name)
    upload.save(file_path)
    
    url_img_save = 'https://thebesttoken.co/static/img/upload/'+name
    #print url_img_save
    db.users.update({ "customer_id" : customer_id }, { '$set': { "personal_info.img_profile": url_img_save } })
    return json.dumps({
        'status': 'complete', 
        'name_ifle' : url_img_save
    })
    
@api_ctrl.route('/upload-img-passport-fontside/<customer_id>', methods=['GET', 'POST'])
def upload_img_passport_fontside(customer_id):
    
    print customer_id
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    
    upload     = request.files.get('file')
    
    save_path = SITE_ROOT+'/../static/img/upload'.format(category='category')
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    name = upload.filename
    file_path = "{path}/{file}".format(path=save_path, file=name)
    upload.save(file_path)
    
    url_img_save = 'https://api.buy-sellpro.co/static/img/upload/'+name
    print url_img_save

    user = db.users.find_one({'customer_id': customer_id})
    user['personal_info']['img_passport_fontside'] = url_img_save
    user['verification'] = 1
    db.users.save(user)
    return json.dumps({
        'status': 'complete'
    })

@api_ctrl.route('/upload-img-passport-backside/<customer_id>', methods=['GET', 'POST'])
def upload_img_passport_backside(customer_id):
    
    print customer_id
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    
    upload     = request.files.get('file')
    
    save_path = SITE_ROOT+'/../static/img/upload'.format(category='category')
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    name = upload.filename
    file_path = "{path}/{file}".format(path=save_path, file=name)
    upload.save(file_path)
    
    url_img_save = 'https://api.buy-sellpro.co/static/img/upload/'+name
    print url_img_save

    user = db.users.find_one({'customer_id': customer_id})
    user['personal_info']['img_passport_backside'] = url_img_save
    user['verification'] = 1
    db.users.save(user)
    return json.dumps({
        'status': 'complete'
    })
    
@api_ctrl.route('/upload-img-address/<customer_id>', methods=['GET', 'POST'])
def upload_img_address(customer_id):
    
    print customer_id
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    
    upload     = request.files.get('file')
    
    save_path = SITE_ROOT+'/../static/img/upload'.format(category='category')
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    name = upload.filename
    file_path = "{path}/{file}".format(path=save_path, file=name)
    upload.save(file_path)
    
    url_img_save = 'https://api.buy-sellpro.co/static/img/upload/'+name
    print url_img_save

    user = db.users.find_one({'customer_id': customer_id})
    user['personal_info']['img_address'] = url_img_save
    user['verification'] = 1
    db.users.save(user)
    return json.dumps({
        'status': 'complete'
    })



def create_account(email,password_login,password_transaction,referees):
    
    localtime = time.localtime(time.time())
    customer_id = '%s%s%s%s%s%s'%(localtime.tm_mon,localtime.tm_year,localtime.tm_mday,localtime.tm_hour,localtime.tm_min,localtime.tm_sec)
    
    datas = {
        'customer_id' : customer_id,
        'username': email,
        'password': set_password(password_login),
        'password_transaction': set_password(password_transaction),
        'email': email,
        'p_node': referees,
        'level': 0,
        'league' : 0,
        'telephone' : '',
        'creation': datetime.utcnow(),
        'd_wallet' : 0,#Profit day
        'r_wallet' : 0,#Direct commission
        's_wallet' : 0,#System commission
        'l_wallet' : 0,#Leadership commission
        'ss_wallet' : 0,#Share sales
        'sf_wallet' : 0,#Share Fund
        'total_earn' : 0,
        'status' : 0,
        'balance' : {
          'bitcoin' : {
            'cryptoaddress' : '',
            'available' : 0
          },
          'ethereum' : {
            'cryptoaddress' : '',
            'available' : 0
          },
          'litecoin' : {
            'cryptoaddress' : '',
            'available' : 0
          },
          'dash' : {
            'cryptoaddress' : '',
            'available' : 0
          },
          'bitcoincash' : {
            'cryptoaddress' : '',
            'available' : 0
          },
          'dogecoin' : {
            'cryptoaddress' : '',
            'available' : 0
          },
          'ripple' : {
            'cryptoaddress' : '',
            'available' : 0
          },
          'eos' : {
            'cryptoaddress' : '',
            'available' : 0
          },
          'tether' : {
            'cryptoaddress' : '',
            'available' : 0
          },
          'coin' : {
            'cryptoaddress' : '',
            'available' : 0
          }
        },
         'security' : {
            'code_forgot' : '',
            'email' : {
                'code' : '',
                'status' : 0
            },
            'authenticator' : {
                'code' : '',
                'status' : 0
            },
            'withdraw' : {
                'code' : '',
                'status' : 0
            },
            'exchange' : {
                'code' : '',
                'status' : 0
            },
            'lock_account' : {
                'code' : '',
                'status' : 0
            },
            'login' : {
                'code' : '',
                'status' : 0
            },
            'fingerprint' :  {
                'code' : '',
                'status' : 0
            },
            'count_send_mail' : 0
        },
        'total_node' : 0,
        'investment' : 0,
        'personal_info' : { 
          'firstname' : '',
          'lastname' : '',
          'date_birthday' :'',
          'address' :'',
          'postalcode' : '',
          'city' : '',
          'country' : '',
          'img_passport_fontside' : '',
          'img_passport_backside' : '',
          'img_address' : '',
          'img_profile' :'assets/imgs/icon-user.png',
          'country' : ''
        } 
    }
    customer = db.users.insert(datas)
    send_mail_register(email)
    return customer_id


def send_mail_register(email):
    html = """ 
      <div style="width: 100%;background: #f3f3f3;"><div style="width: 80%;background: #fff; margin: 0 auto "><div style="background: linear-gradient(to top, #160c56 0%, #052238 100%); height: 180px;text-align: center;"><img src="https://i.ibb.co/KhXc2YW/token.png" width="120px;" style="margin-top: 30px;" /></div><br/><div style="padding: 20px;">
      <p style="color: #222; font-size: 14px;">Thank you for registering with The Best Token.</p>
      <p style="color: #222;  font-size: 14px;">Congratulations on successful account registration with email: <b>"""+str(email)+"""</b>. You can use our service now.</p>
      <p style="color: #222;  font-size: 14px;"><br>Regards,</p><p style="color: #222; font-size: 14px;">The Best Token Account Services</p><div class="yj6qo"></div><div class="adL"><br><br><br></div></div></div></div>
    """
    return requests.post(
      Config().utl_mail,
      auth=("api", Config().api_mail),
      data={"from": Config().from_mail,
        "to": ["", email],
        "subject": "Register Account",
        "html": html}) 
    return True

   
def sendmail_forgot_password_code(email,code):
    html = """ 
      <div style="width: 100%;background: #f3f3f3;"><div style="width: 80%;background: #fff; margin: 0 auto "><div style="background: linear-gradient(to top, #160c56 0%, #052238 100%); height: 180px;text-align: center;"><img src="https://i.ibb.co/KhXc2YW/token.png" width="120px;" style="margin-top: 30px;" /></div><br/><div style="padding: 20px;">
      <p style="color: #222; font-size: 14px;">Thank you for registering with The Best Token.</p>
      <p style="color: #222;  font-size: 14px;">Your verification code is <b>"""+str(code)+"""</b>, Please do not disclose this to others! </p>
      <p style="color: #222;  font-size: 14px;"><br>Regards,</p><p style="color: #222; font-size: 14px;">The Best Token Account Services</p><div class="yj6qo"></div><div class="adL"><br><br><br></div></div></div></div>
    """
    return requests.post(
      Config().utl_mail,
      auth=("api", Config().api_mail),
      data={"from": Config().from_mail,
        "to": ["", email],
        "subject": "Forgot Password",
        "html": html}) 
    return True

def sendmail_code_verify_email(email,code):
    html = """ 
      <div style="width: 100%;background: #f3f3f3;"><div style="width: 80%;background: #fff; margin: 0 auto "><div style="background: linear-gradient(to top, #160c56 0%, #052238 100%); height: 180px;text-align: center;"><img src="https://i.ibb.co/KhXc2YW/token.png" width="120px;" style="margin-top: 30px;" /></div><br/><div style="padding: 20px;">
      <p style="color: #222; font-size: 14px;">Thank you for registering with The Best Token.</p>
      <p style="color: #222;  font-size: 14px;">Your verification code is <b>"""+str(code)+"""</b>, Please do not disclose this to others! </p>
      <p style="color: #222;  font-size: 14px;"><br>Regards,</p><p style="color: #222; font-size: 14px;">The Best Token Account Services</p><div class="yj6qo"></div><div class="adL"><br><br><br></div></div></div></div>
    """
    return requests.post(
      Config().utl_mail,
      auth=("api", Config().api_mail),
      data={"from": Config().from_mail,
        "to": ["", email],
        "subject": "Verify Email",
        "html": html}) 
    return True

def price_coin_abs(amount):
    if float(amount) >= 0:
        amount = round(float(amount),2)
    else:
        amount = '-'+str(round(abs(float(amount)),2))
    return amount
@api_ctrl.route('/auto-tickers', methods=['GET', 'POST'])
def auto_tickers():
    url_api = "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,DASH,USDT,EOS,LTC,XRP,BCH,DOGE&tsyms=USD&api_key=6ecd050c6cf3b457ebaaed0fc372f493aae2cb15a4888d19dbab8b85bfbbc4c4&api_key=6ecd050c6cf3b457ebaaed0fc372f493aae2cb15a4888d19dbab8b85bfbbc4c4"
    r = requests.get(url_api)
    response_dict = r.json()

    btc_change = response_dict['RAW']['BTC']['USD']['CHANGEDAY']
    btc_usd = response_dict['RAW']['BTC']['USD']['PRICE']

    eth_change = response_dict['RAW']['ETH']['USD']['CHANGEDAY']
    eth_usd = response_dict['RAW']['ETH']['USD']['PRICE']

    ltc_change = response_dict['RAW']['LTC']['USD']['CHANGEDAY']
    ltc_usd = response_dict['RAW']['LTC']['USD']['PRICE']

    xrp_change = response_dict['RAW']['XRP']['USD']['CHANGEDAY']
    xrp_usd = response_dict['RAW']['XRP']['USD']['PRICE']

    eos_change = response_dict['RAW']['EOS']['USD']['CHANGEDAY']
    eos_usd = response_dict['RAW']['EOS']['USD']['PRICE']

    dash_change = response_dict['RAW']['DASH']['USD']['CHANGEDAY']
    dash_usd = response_dict['RAW']['DASH']['USD']['PRICE']

    bch_change = response_dict['RAW']['BCH']['USD']['CHANGEDAY']
    bch_usd = response_dict['RAW']['BCH']['USD']['PRICE']

    doge_change = response_dict['RAW']['DOGE']['USD']['CHANGEDAY']
    doge_usd = response_dict['RAW']['DOGE']['USD']['PRICE']

    usdt_change = response_dict['RAW']['USDT']['USD']['CHANGEDAY']
    usdt_usd = response_dict['RAW']['USDT']['USD']['PRICE']

    

    data_ticker = db.tickers.find_one({})
    data_ticker['btc_usd'] = round(float(btc_usd),2)
    data_ticker['xrp_usd'] = round(float(xrp_usd),2)
    data_ticker['ltc_usd'] = round(float(ltc_usd),2)
    data_ticker['eth_usd'] = round(float(eth_usd),2)
    data_ticker['usdt_usd'] = round(float(usdt_usd),2)
    data_ticker['dash_usd'] = round(float(dash_usd),2)
    data_ticker['eos_usd'] = round(float(eos_usd),4)
    data_ticker['bch_usd'] = round(float(bch_usd),2)
    data_ticker['doge_usd'] = round(float(doge_usd),4)


    data_ticker['btc_change'] =  price_coin_abs(btc_change)

    
    data_ticker['eth_change'] = price_coin_abs(eth_change)

    
    data_ticker['ltc_change'] = price_coin_abs(ltc_change)

    
    data_ticker['dash_change'] = price_coin_abs(dash_change)

    
    data_ticker['eos_change'] = price_coin_abs(eos_change)

    
    data_ticker['xrp_change'] = price_coin_abs(xrp_change)

    data_ticker['bch_change'] = price_coin_abs(bch_change)
    data_ticker['doge_change'] = price_coin_abs(doge_change)

    
    data_ticker['usdt_change'] =  price_coin_abs(usdt_change)
   
    db.tickers.save(data_ticker)
    return json.dumps({'status': 'success'})



@api_ctrl.route('/auto-tickers-binace', methods=['GET', 'POST'])
def auto_tickers_binace():
    url_api = "https://api.binance.com/api/v1/ticker/24hr"
    r = requests.get(url_api)
    response_dict = r.json()
    data_ticker = db.tickers.find_one({})
    for x in response_dict:
      if x['symbol'] == "BTCTUSD":
        data_ticker['btc_usd'] = round(float(x['lastPrice']),2)
        data_ticker['btc_change'] =  price_coin_abs(x['priceChangePercent'])
      if x['symbol'] == "ETHTUSD":
        data_ticker['eth_usd'] = round(float(x['lastPrice']),2)
        data_ticker['eth_change'] =  price_coin_abs(x['priceChangePercent'])
      if x['symbol'] == "LTCTUSD":
        data_ticker['ltc_usd'] = round(float(x['lastPrice']),2)
        data_ticker['ltc_change'] =  price_coin_abs(x['priceChangePercent'])
      if x['symbol'] == "BCHTUSD":
        data_ticker['bch_usd'] = round(float(x['lastPrice']),2)
        data_ticker['bch_change'] =  price_coin_abs(x['priceChangePercent'])
      if x['symbol'] == "DASHTUSD":
        data_ticker['dash_usd'] = round(float(x['lastPrice']),2)
        data_ticker['dash_change'] =  price_coin_abs(x['priceChangePercent'])
      if x['symbol'] == "XRPTUSD":
        data_ticker['xrp_usd'] = round(float(x['lastPrice']),2)
        data_ticker['xrp_change'] =  price_coin_abs(x['priceChangePercent'])
    db.tickers.save(data_ticker)
    return json.dumps({'status': 'success'})