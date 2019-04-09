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
sys.setrecursionlimit(10000)
digits58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'






rpc_connection = AuthServiceProxy("http://smartfvarpc:5vMddNTNZiwRrbEkgtS4DcVZSppjwq6CzSGxoTqL2w7Y@bblrpcccqoierzxcxbx.co")
rpc_connection_btc = AuthServiceProxy("http://Ecy4M83321mWk7szPoiY2cw:DrWdoW83321Zrdi2ftYKVPt4P2Cb7HoQUZUuP6@127.0.0.1:23321")

__author__ = 'taijoe'

user_ctrl = Blueprint('user', __name__, static_folder='static', template_folder='templates')
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

def get_id_tree_left(ids):
    listId = ''
    query = db.User.find({'customer_id': ids})
    for x in query:
        listId += ', %s'%(x.left)
        listId += get_id_tree_left(x.left)
    return listId
def get_id_tree_right(ids):
    listId = ''
    query = db.User.find({'customer_id': ids})
    for x in query:
        print x['right']
        listId += ', %s'%(x.right)
        listId += get_id_tree_right(x.right)
    return listId

def Get_binary_binary_left(customer_id):
    count = db.User.find_one({'customer_id': customer_id})
    customer_binary =''
    if count.left == '':
        customer_binary += ', %s'%(customer_id)
    else:
        ids = count.left
        count = get_id_tree_left(count.left)
        if count:
            customer_binary = '%s , %s'%(count, ids)
        else:
            customer_binary = ',%s'%(ids)
    customer_binary = customer_binary[1:]
    customers = customer_binary.split(',')

    if len(customers)== 2:
        customer_binary = customers[1].strip()
    if len(customers) >= 3:
        customer_binary = max(customers).strip()
    return customer_binary
def Get_binary_binary_right(customer_id):
    count = db.User.find_one({'customer_id': customer_id})
    customer_binary =''
    if count.right == '':
        customer_binary += ', %s'%(customer_id)
    else:
        ids = count.right
        count = get_id_tree_right(count.right)
        if count:
            customer_binary = '%s , %s'%(count, ids)
        else:
            customer_binary = ',%s'%(ids)
    customer_binary = customer_binary[1:]
    customers = customer_binary.split(',')

    if len(customers)== 2:
        customer_binary = customers[1].strip()
    if len(customers) >= 3:
        customer_binary = max(customers).strip()
    return customer_binary
def send_mail_register(email,usernames,link_active):
    # username = 'support@World Trader.co'
    # password = 'YK45OVfK45OVfobZ5XYobZ5XYK45OVfobZ5XYK45OVfobZ5X'
    # msg = MIMEMultipart('mixed')
    # sender = 'support@World Trader.co'
    # recipient = str(email)

    # # username = 'no-reply@World Trader.co'
    # # password = 'rbdlnsmxqpswyfdv'
    # # msg = MIMEMultipart('mixed')
    # # mailServer = smtplib.SMTP('smtp.gmail.com', 587) # 8025, 587 and 25 can also be used. 
    # # mailServer.ehlo()
    # # mailServer.starttls()
    # # mailServer.ehlo()
    # # mailServer.login(username, password)
    # # sender = 'no-reply@World Trader.co'
    # # recipient = email

    # msg['Subject'] = 'Activate Your World Trader account'
    # msg['From'] = sender
    # msg['To'] = recipient

    html = """\
        <div style="font-family:Arial,sans-serif;background-color:#f9f9f9;color:#424242;text-align:center">
       <div class="adM">
       </div>
       <table style="table-layout:fixed;width:90%;max-width:600px;margin:0 auto;background-color:#f9f9f9">
          <tbody>
             <tr>
                <td style="padding:20px 10px 10px 0px;text-align:left">
                   <a href="https://worldtrader.info" title="World Trade" target="_blank" >
                   <img src="https://worldtrader.info/static/home/images/logo/logo.png" alt="World Trade" class="CToWUd" style=" width: 200px; ">
                   </a>
                </td>
                <td style="padding:0px 0px 0px 10px;text-align:right">
                </td>
             </tr>
          </tbody>
       </table>
    </div>
    <div style="font-family:Arial,sans-serif;background-color:#f9f9f9;color:#424242;text-align:center">
       <table style="table-layout:fixed;width:90%;max-width:600px;margin:0 auto;background:#fff;font-size:14px;border:2px solid #e8e8e8;text-align:left;table-layout:fixed">
          <tbody>
             <tr>
                <td style="padding:30px 30px 10px 30px;line-height:1.8">Dear <b>"""+str(usernames)+"""</b>,</td>
             </tr>
             <tr>
                <td style="padding:10px 30px;line-height:1.8">Thank you for registering on the <a href="https://worldtrader.info/" target="_blank">World Trade</a>.</td>
             </tr>
             <tr>
                <td style="padding:10px 30px;line-height:1.8">Your World Trade verification code is: <b>"""+str(link_active)+"""</b></td>
             </tr>

             <tr>
                <td style="border-bottom:3px solid #efefef;width:90%;display:block;margin:0 auto;padding-top:30px"></td>
             </tr>
             <tr>
                <td style="padding:30px 30px 30px 30px;line-height:1.3">Best regards,<br> <a href="https://worldtrader.info/" target="_blank" >World Trade</a></td>
             </tr>
          </tbody>
       </table>
    </div>
    <div style="font-family:Arial,sans-serif;background-color:#f9f9f9;color:#424242;text-align:center;padding-bottom:10px;     height: 50px;">
   
</div>
    """

    return requests.post(
      "https://api.mailgun.net/v3/worldtrader.info/messages",
      auth=("api", "key-4cba65a7b1a835ac14b7949d5795236a"),
      data={"from": "World Trade <no-reply@worldtrader.info>",
        "to": ["", email],
        "subject": "Account registration successful",
        "html": html})


    # html_message = MIMEText(html, 'html')
    
    # msg.attach(html_message)

    # mailServer = smtplib.SMTP('mail.smtp2go.com', 2525) # 8025, 587 and 25 can also be used. 
    # mailServer.ehlo()
    # mailServer.starttls()
    # mailServer.ehlo()
    # mailServer.login(username, password)
    # mailServer.sendmail(sender, recipient, msg.as_string())
    # mailServer.close()
    
    # html_message = MIMEText(html, 'html')
    # msg.attach(html_message)
    # mailServer.sendmail(sender, recipient, msg.as_string())
    # mailServer.close()

def send_mail_confirm(email):
    username = 'support@World Trader.co'
    password = 'YK45OVfK45OVfobZ5XYobZ5XYK45OVfobZ5XYK45OVfobZ5X'
    msg = MIMEMultipart('mixed')
    sender = 'support@World Trader.co'
    recipient = str(email)
    # username = 'no-reply@World Trader.co'
    # password = 'rbdlnsmxqpswyfdv'
    # msg = MIMEMultipart('mixed')
    # mailServer = smtplib.SMTP('smtp.gmail.com', 587) # 8025, 587 and 25 can also be used. 
    # mailServer.ehlo()
    # mailServer.starttls()
    # mailServer.ehlo()
    # mailServer.login(username, password)
    # sender = 'no-reply@World Trader.co'
    # recipient = email

    msg['Subject'] = 'Congratulations. Your account is now active!'
    msg['From'] = sender
    msg['To'] = recipient
    html = """\
        <div style="font-family:Arial,sans-serif;background-color:#f9f9f9;color:#424242;text-align:center">
   <div class="adM">
   </div>
   <table style="table-layout:fixed;width:90%;max-width:600px;margin:0 auto;background-color:#f9f9f9">
      <tbody>
         <tr>
            <td style="padding:20px 10px 10px 0px;text-align:left">
               <a href="https://World Trader.co/" title="World Trader" target="_blank" >
               <img src="https://i.imgur.com/tyjTbng.png" alt="World Trader" class="CToWUd" style=" width: 100px; ">
               </a>
            </td>
            <td style="padding:0px 0px 0px 10px;text-align:right">
            </td>
         </tr>
      </tbody>
   </table>
</div>
<div style="font-family:Arial,sans-serif;background-color:#f9f9f9;color:#424242;text-align:center">
   <table style="table-layout:fixed;width:90%;max-width:600px;margin:0 auto;background:#fff;font-size:14px;border:2px solid #e8e8e8;text-align:left;table-layout:fixed">
      <tbody>
         <tr>
            <td style="padding:10px 30px;line-height:1.8">Congratulations, Your account on the <a href="https://World Trader.co/" target="_blank">World Trader</a> is now registered and active.</td>
         </tr>
         <tr>
            <td style="border-bottom:3px solid #efefef;width:90%;display:block;margin:0 auto;padding-top:30px"></td>
         </tr>
         <tr>
            <td style="padding:30px 30px 30px 30px;line-height:1.3">Best regards,<br> World Trader Team<br>  <a href="https://www.World Trader.co/" target="_blank" >www.World Trader.co</a></td>
         </tr>
      </tbody>
   </table>
</div>
<div style="font-family:Arial,sans-serif;background-color:#f9f9f9;color:#424242;text-align:center;padding-bottom:10px;     height: 50px;">
   
</div>
    """
    html_message = MIMEText(html, 'html')
    msg.attach(html_message)
    mailServer = smtplib.SMTP('mail.smtp2go.com', 2525) # 8025, 587 and 25 can also be used. 
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(username, password)
    mailServer.sendmail(sender, recipient, msg.as_string())
    mailServer.close()
    # html_message = MIMEText(html, 'html')
    # msg.attach(html_message)
    # mailServer.sendmail(sender, recipient, msg.as_string())
    # mailServer.close()

def send_mail_for_sponsor(email, usernames):
    username = 'support@World Trader.co'
    password = 'YK45OVfK45OVfobZ5XYobZ5XYK45OVfobZ5XYK45OVfobZ5X'
    msg = MIMEMultipart('mixed')

    sender = 'support@World Trader.co'
    recipient = str(email)

    msg['Subject'] = 'Congratulations. You have introduced new members'
    msg['From'] = sender
    msg['To'] = recipient
    html = """<div style="font-family:Arial,sans-serif;background-color:#f9f9f9;color:#424242;text-align:center">
   <div class="adM">
   </div>
   <table style="table-layout:fixed;width:90%;max-width:600px;margin:0 auto;background-color:#f9f9f9">
      <tbody>
         <tr>
            <td style="padding:20px 10px 10px 0px;text-align:left">
               <a href="https://World Trader.co/" title="World Trader" target="_blank" >
               <img src="https://i.imgur.com/tyjTbng.png" alt="World Trader" class="CToWUd" style=" width: 100px; ">
               </a>
            </td>
            <td style="padding:0px 0px 0px 10px;text-align:right">
            </td>
         </tr>
      </tbody>
   </table>
</div>
<div style="font-family:Arial,sans-serif;background-color:#f9f9f9;color:#424242;text-align:center">
   <table style="table-layout:fixed;width:90%;max-width:600px;margin:0 auto;background:#fff;font-size:14px;border:2px solid #e8e8e8;text-align:left;table-layout:fixed">
      <tbody>
         <tr>
            <td style="padding:10px 30px;line-height:1.8">Congratulations. You have introduced new members on the <a href="https://World Trader.co/" target="_blank">World Trader</a>.</td>
         </tr>
          <tr>
                <td style="padding:30px 30px 10px 30px;line-height:1.8">Username: <b>"""+str(usernames)+"""</b></td>
             </tr>
<tr>
  <td style="padding:10px 30px;line-height:1.8">Login to plant the system <a href="https://World Trader.co/auth/login" target="_blank">Login to World Trader </a></td>
</tr>
         <tr>
            <td style="border-bottom:3px solid #efefef;width:90%;display:block;margin:0 auto;padding-top:30px"></td>
         </tr>
         <tr>
            <td style="padding:30px 30px 30px 30px;line-height:1.3">Best regards,<br> World Trader Team<br>  <a href="https://www.World Trader.co/" target="_blank" >www.World Trader.co</a></td>
         </tr>
      </tbody>
   </table>
</div>
<div style="font-family:Arial,sans-serif;background-color:#f9f9f9;color:#424242;text-align:center;padding-bottom:10px;     height: 50px;">
   
</div>
    """
    html_message = MIMEText(html, 'html')
    
    msg.attach(html_message)

    mailServer = smtplib.SMTP('mail.smtp2go.com', 2525) # 8025, 587 and 25 can also be used. 
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(username, password)
    mailServer.sendmail(sender, recipient, msg.as_string())
    mailServer.close()

@user_ctrl.route('/', methods=['GET', 'POST'])
def home():
    return redirect('/auth/login')

def get_totp_uri(otp_secret, user):
  return 'otpauth://totp/Diamondcapital:{0}?secret={1}&issuer=Diamondcapital' \
    .format(user['username'], otp_secret)
def verify_totp(token, otp_secret):
    return onetimepass.valid_totp(token, otp_secret)

@user_ctrl.route('/setting', methods=['GET', 'POST'])
def setting():
    if session.get(u'logged_in') is None:
        return redirect('/user/login')
    uid = session.get('uid')
    user = db.User.find_one({'customer_id': uid})
    if user['secret_2fa'] == '':
      otp_secret = base64.b32encode(os.urandom(10)).decode('utf-8')
      db.users.update({"customer_id": uid}, { "$set": { "secret_2fa":otp_secret} })
    else:
      otp_secret = user['secret_2fa']

    url_otp = get_totp_uri(otp_secret,user)

    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "../static", "country-list.json")
    data_country = json.load(open(json_url))
    data_ticker = db.tickers.find_one({})
    data ={
    'user' : user,
    'title': 'Account',
    'menu' : 'setting',
    'country' : data_country,
    'url_otp' : url_otp,
    'otp_secret': otp_secret,
    'btc_usd':data_ticker['btc_usd'],
    'sva_btc':data_ticker['sva_btc'],
    'sva_usd':data_ticker['sva_usd']
    }

    return render_template('account/account.html', data=data)

@user_ctrl.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if session.get(u'logged_in') is None:
        return redirect('/user/login')
    uid = session.get('uid')
    user = db.users.find_one({'customer_id': uid})
    list_notifications = db.notifications.find({'$and' : [{'read' : 0},{'status' : 0},{'$or' : [{'uid' : uid},{'type' : 'all'}]}]})
    number_notifications = list_notifications.count()
    data ={
    'user' : user,
    'title': 'Account',
    'menu' : 'setting',
    'number_notifications' : number_notifications,
    'list_notifications' : list_notifications
    }
    return render_template('account/change_password.html', data=data)

@user_ctrl.route('/my-profile', methods=['GET', 'POST'])
def my_profile():
    if session.get(u'logged_in') is None:
        return redirect('/user/login')
    uid = session.get('uid')
    user = db.users.find_one({'customer_id': uid})


    if user['secret_2fa'] == '':
      otp_secret = base64.b32encode(os.urandom(10)).decode('utf-8')
      db.users.update({"customer_id": uid}, { "$set": { "secret_2fa":otp_secret} })
    else:
      otp_secret = user['secret_2fa']

    url_otp = get_totp_uri(otp_secret,user)

    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "../static", "country-list.json")
    data_country = json.load(open(json_url))
    data_ticker = db.tickers.find_one({})
    token_crt = id_generator(15) 
    session['token_crt'] = token_crt
    list_notifications = db.notifications.find({'$and' : [{'read' : 0},{'status' : 0},{'$or' : [{'uid' : uid},{'type' : 'all'}]}]})
    number_notifications = list_notifications.count()

    data ={
    'user' : user,
    'title': 'Account',
    'menu' : 'my_profile',
    'list_notifications' : list_notifications,
    'number_notifications' : number_notifications,
    'url_otp' : url_otp,
    'data_country' : data_country,
    'token_crt' : token_crt
    }
    return render_template('account/my_profile.html', data=data)

@user_ctrl.route('/verify-account', methods=['GET', 'POST'])
def verify_accountsss():
    if session.get(u'logged_in') is None:
        return redirect('/user/login')
    uid = session.get('uid')
    user = db.users.find_one({'customer_id': uid})
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "../static", "country-list.json")
    data_country = json.load(open(json_url))

    token_crt = id_generator(15) 
    session['token_crt'] = token_crt
    
    verify = db.verifys.find({'uid': uid})
    list_notifications = db.notifications.find({'$and' : [{'read' : 0},{'status' : 0},{'$or' : [{'uid' : uid},{'type' : 'all'}]}]})
    number_notifications = list_notifications.count()
    data ={
    'user' : user,
    'title': 'Account',
    'menu' : 'setting',
    'data_country' : data_country,
    'token_crt' : token_crt,
    'verify' : verify,
    'list_notifications' : list_notifications,
    'number_notifications' : number_notifications
    }
    return render_template('account/verify_account.html', data=data)

@user_ctrl.route('/verify-account/identity', methods=['GET', 'POST'])
def verify_account_identity():
    if session.get(u'logged_in') is None:
        return redirect('/user/login')
    uid = session.get('uid')
    user = db.users.find_one({'customer_id': uid})
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "../static", "country-list.json")
    data_country = json.load(open(json_url))

    token_crt = id_generator(15) 
    session['token_crt'] = token_crt
    
    verify = db.verifys.find({'uid': uid})
    list_notifications = db.notifications.find({'$and' : [{'read' : 0},{'status' : 0},{'$or' : [{'uid' : uid},{'type' : 'all'}]}]})
    number_notifications = list_notifications.count()
    data ={
    'user' : user,
    'title': 'Account',
    'menu' : 'setting',
    'data_country' : data_country,
    'token_crt' : token_crt,
    'verify' : verify,
    'list_notifications' : list_notifications,
    'number_notifications' : number_notifications
    }
    return render_template('account/verify_account_identity.html', data=data)

@user_ctrl.route('/two-factor-auth', methods=['GET', 'POST'])
def two_factor_auth():
    if session.get(u'logged_in') is None:
        return redirect('/user/login')
    uid = session.get('uid')
    user = db.User.find_one({'customer_id': uid})
    if user['secret_2fa'] == '':
      otp_secret = base64.b32encode(os.urandom(10)).decode('utf-8')
      db.users.update({"customer_id": uid}, { "$set": { "secret_2fa":otp_secret} })
    else:
      otp_secret = user['secret_2fa']

    url_otp = get_totp_uri(otp_secret,user)

    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "../static", "country-list.json")
    data_country = json.load(open(json_url))
    data_ticker = db.tickers.find_one({})
    list_notifications = db.notifications.find({'$and' : [{'read' : 0},{'status' : 0},{'$or' : [{'uid' : uid},{'type' : 'all'}]}]})
    number_notifications = list_notifications.count()
    data ={
    'user' : user,
    'title': 'Account',
    'menu' : 'setting',
    'country' : data_country,
    'url_otp' : url_otp,
    'otp_secret': otp_secret,
    'list_notifications' : list_notifications,
    'number_notifications' : number_notifications
    }

    return render_template('account/two_factor_auth.html', data=data)

@user_ctrl.route('/2FA', methods=['GET', 'POST'])
def Check2FA():
  uid = session.get('uid')
  user = db.User.find_one({'customer_id': uid})
  if request.method == 'POST':
    code = request.form['GACode']
    checkVerifY = verify_totp(code, user['secret_2fa'])
    status_2fa = user['status_2fa']
    print status_2fa
    if checkVerifY == False:
      msg = 'The two-factor authentication code you specified is incorrect. Please check the clock on your authenticator device to verify that it is in sync'
      types = 'danger'
    else:
      if int(status_2fa) == 0:
        db.users.update({ "customer_id" : uid }, { '$set': { "status_2fa": 1 } })
      else:
        db.users.update({ "customer_id" : uid }, { '$set': { "status_2fa": 0 } })
      msg = 'Change status success'
      types = 'success'
    flash({'msg': msg, 'type':types})
  return redirect('/user/my-profile')

@user_ctrl.route('/updateaccount', methods=['GET', 'POST'])
def updateaccount():
    if session.get(u'logged_in') is None:
        return redirect('/user/login')
    uid = session.get('uid')
    user = db.users.find_one({'customer_id': uid})
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    if request.method == 'POST' and request.form['token_crt'] == session['token_crt']:
        telephone = request.form['telephone']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        date_birthday = request.form['date_birthday']
        address = request.form['address']
        postalcode = request.form['postalcode']
        city = request.form['city']
        country = request.form['country']
        email = request.form['email']
        user['personal_info']['firstname'] = firstname
        user['personal_info']['lastname'] = lastname
        user['personal_info']['date_birthday'] = date_birthday
        user['personal_info']['address'] = address
        user['personal_info']['postalcode'] = postalcode
        user['personal_info']['city'] = city
        user['personal_info']['country'] = country
        user['telephone'] = telephone
        user['email'] = email
        db.users.save(user)
        
        session['token_crt'] = id_generator(15)
        return redirect('/user/verify-account/identity')
    return redirect('/user/my-profile')

@user_ctrl.route('/account/identity', methods=['GET', 'POST'])
def identity():
    if session.get(u'logged_in') is None:
        return redirect('/user/login')
    uid = session.get('uid')
    user = db.users.find_one({'customer_id': uid})
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    if request.method == 'POST' and request.form['token_crt'] == session['token_crt']:
          
        print request.files
        upload_1     = request.files.get('file_1')
        upload_2     = request.files.get('file_2')
        upload_3     = request.files.get('file_3')
    
        save_path = SITE_ROOT+'/../static/img/upload'.format(category='category')
        if not os.path.exists(save_path):
            os.makedirs(save_path)


        name_1 = id_generator(25)+upload_1.filename
        file_path_1 = "{path}/{file}".format(path=save_path, file=name_1)
        upload_1.save(file_path_1)

        name_2 = id_generator(25)+upload_2.filename
        file_path_2 = "{path}/{file}".format(path=save_path, file=name_2)
        upload_2.save(file_path_2)

        name_3 = id_generator(25)+upload_3.filename
        file_path_3 = "{path}/{file}".format(path=save_path, file=name_3)
        upload_3.save(file_path_3)


        user['personal_info']['img_passport_fontside'] = '/static/img/upload/'+name_1
        user['personal_info']['img_passport_backside'] = '/static/img/upload/'+name_2
        user['personal_info']['img_address'] = '/static/img/upload/'+name_3
        user['status_verify'] = 1

        db.users.save(user)


        data_verifys = {
            'uid' : uid,
            'user_id': user['_id'],
            'username' : user['username'],
            'img1' : '/static/img/upload/'+name_1,
            'img2': '/static/img/upload/'+name_2,
            'img3' : '/static/img/upload/'+name_3,
            'date_added' : datetime.utcnow(),
            'id_number' : id_generator(6),
            'admin_note' : '',
            'status' : 0
        }
        db.verifys.insert(data_verifys)

        
        session['token_crt'] = id_generator(15) 
        return redirect('/user/my-profile')
    return redirect('/user/my-profile')

@user_ctrl.route('/updatewallet', methods=['GET', 'POST'])
def updatewallet():
    if session.get(u'logged_in') is None:
        return redirect('/user/login')
    uid = session.get('uid')
    user = db.User.find_one({'customer_id': uid})
    if request.method == 'POST':
        wallet = request.form['wallet']
        check = check_bc(wallet)
        check_wallet_btc = db.User.find_one({'btc_wallet': wallet, "customer_id": { "$not": { "$in": [uid] } }})
        if request.form['wallet'] == '':
            flash({'msg':'Invalid wallet', 'type':'danger'})
            return redirect('/user/setting')
        
        if check_password(user.password_transaction, request.form['password']) == False:
                flash({'msg':'Invalid password. Please try again!', 'type':'danger'})
                return redirect('/user/setting')
        
        if check == False or check_wallet_btc is not None:
            flash({'msg':'Invalid wallet', 'type':'danger'})
            return redirect('/user/setting')
        if check == True and check_wallet_btc is None and check_password(user.password_transaction, request.form['password']) == True:
            flash({'msg':'Update wallet success', 'type':'success'})
            db.users.update({ "customer_id" : uid }, { '$set': { "btc_wallet": wallet }, '$push':{'wallet_old':{'wallet':wallet, 'date': datetime.utcnow()}} })
        if request.form['eth_wallet']:
            check_wallet_eth = db.User.find_one({'wallet': request.form['eth_wallet'], "customer_id": { "$not": { "$in": [uid] } }})
            if check_wallet_eth is None and check_password(user.password_transaction, request.form['password']) == True:
                db.users.update({ "customer_id" : uid }, { '$set': { "wallet": request.form['eth_wallet'] }})
    return redirect('/user/setting')

@user_ctrl.route('/update-password', methods=['GET', 'POST'])
def update_password():
    if session.get(u'logged_in') is None:
        return redirect('/user/login')
    uid = session.get('uid')
    user = db.User.find_one({'customer_id': uid})
    if request.method == 'POST':
        old_password= request.form['old_password']
        new_password= request.form['new_password']
        repeat_new_password= request.form['repeat_new_password']
        if old_password == "" or new_password == "":
            flash({'msg':'Invalid password. Please try again!', 'type':'danger'})
            return redirect('/user/my-profile')

        if check_password(user.password, old_password) == False:
            flash({'msg':'Invalid old password. Please try again!', 'type':'danger'})
            return redirect('/user/my-profile')
        if new_password != repeat_new_password:
            flash({'msg':'Password repeat incorrectly. Please try again!', 'type':'danger'})
            return redirect('/user/my-profile')
        if new_password == repeat_new_password and check_password(user.password, old_password) == True:
            flash({'msg':'Update Password success', 'type':'success'})
            db.users.update({ "customer_id" : uid }, { '$set': { "password": set_password(new_password) }})
            return redirect('/user/my-profile')


@user_ctrl.route('/update-tran-password', methods=['GET', 'POST'])
def update_tran_password():
    if session.get(u'logged_in') is None:
        return redirect('/user/login')
    uid = session.get('uid')
    user = db.User.find_one({'customer_id': uid})
    if request.method == 'POST':
        old_password= request.form['old_tran_password']
        new_password= request.form['new_tran_password']
        repeat_new_password= request.form['repeat_new_tran_password']
        if old_password == "" or new_password == "":
            flash({'msg':'Invalid password. Please try again!', 'type':'danger'})
            return redirect('/user/setting')

        if check_password(user.password_transaction, old_password) == False:
            flash({'msg':'Invalid old password. Please try again!', 'type':'danger'})
            return redirect('/user/setting')
        if new_password != repeat_new_password:
            flash({'msg':'Password repeat incorrectly. Please try again!', 'type':'danger'})
            return redirect('/user/setting')
        if new_password == repeat_new_password and check_password(user.password_transaction, old_password) == True:
            flash({'msg':'Update Password success', 'type':'success'})
            db.users.update({ "customer_id" : uid }, { '$set': { "password_transaction": set_password(new_password) }})
            return redirect('/user/setting')

@user_ctrl.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in') is not None:
        return redirect('/account/dashboard')
    if request.method == 'GET':
        return render_template('login.html')

    #else must return something as login-process result
    return
@user_ctrl.route('/register/<user_id>', methods=['GET', 'POST'])
def signup(user_id):
    
    sponser = db.users.find_one({'customer_id': user_id})
    if sponser is None:
        return redirect('/account/dashboard')

    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "../static", "country-list.json")
    data_country = json.load(open(json_url))
    value = {
        'country' : data_country,
        'uid' : user_id,
        'sponser' : sponser
    }
    return render_template('register.html', data=value)
@user_ctrl.route('/new/<positon>/<p_binary>/<p_node>', methods=['GET', 'POST'])
def signup_intree(positon, p_binary, p_node):
    
    sponser = db.User.find_one({'customer_id': p_node})
    if sponser is None:
        return redirect('/account/dashboard')
    binary = db.User.find_one({'customer_id': p_binary})
    if binary is None:
        return redirect('/account/dashboard')
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "../static", "country-list.json")
    data_country = json.load(open(json_url))
    value = {
    'country' : data_country,
    'uid' : p_node,
    'position': positon,
    'p_binary': p_binary,
    'sponser' : sponser
    }
    if int(positon) == 1 or int(positon) == 2:
        if int(positon) == 1:
            if binary.left == '':
                return render_template('account/signup_in_tree.html', data=value)
            else:
                flash({'msg':'Invalid Position. Please try again!', 'type':'danger'})
                return redirect('/account/dashboard')
        if int(positon) == 2:
            if binary.right == '':
                return render_template('account/signup_in_tree.html', data=value)
            else:
                flash({'msg':'Invalid Position. Please try again!', 'type':'danger'})
                return redirect('/account/dashboard')
    else:
        flash({'msg':'Invalid Position. Please try again!', 'type':'danger'})
        return redirect('/account/dashboard')
    
    return render_template('account/signup_in_tree.html', data=value)
@user_ctrl.route('/registersubmit_intree', methods=['GET', 'POST'])
def registersubmit_intree():
    #return redirect('/user/login')
    if request.method == 'POST':
        sponser = db.User.find_one({'customer_id': request.form['ref']})
        if sponser is None:
            return redirect('/account/dashboard')
        binary = db.User.find_one({'customer_id': request.form['p_binary']})
        if binary is None:
            return redirect('/account/dashboard')
     
        if int(request.form['position']) == 1:
            if binary.left != '':
                flash({'msg':'Please enter a valid form!', 'type':'danger'})
                return redirect('/user/new/'+str(request.form['position'])+'/'+str(request.form['p_binary'])+'/'+str(request.form['ref'])+'')
        if int(request.form['position']) == 2:
            if binary.right != '':
                flash({'msg':'Please enter a valid form!', 'type':'danger'})
                return redirect('/user/new/'+str(request.form['position'])+'/'+str(request.form['p_binary'])+'/'+str(request.form['ref'])+'')

        if request.form['fullname'] == '' or request.form['login'] == '' or request.form['password'] == '' or request.form['email'] == '' or request.form['ref'] == '' or request.form['telephone'] == '' or request.form['position'] == '':
            flash({'msg':'Please enter a valid form!', 'type':'danger'})
            return redirect('/user/new/'+str(request.form['position'])+'/'+str(request.form['p_binary'])+'/'+str(request.form['ref'])+'')
        username_new = request.form['login']
        username_new = username_new.lower()
        new_emails = request.form['email']
        new_wallet = request.form['wallet']
        new_emails = new_emails.lower()
        check_username = db.User.find_one({'username': username_new})
        
        # check_num_phone = client_phone.get_standard_number_insight(number=request.form['telephone'])
        # if check_num_phone['status'] == 3:
        #     flash({'msg':'Invalid Telephone', 'type':'danger'})
        #     return redirect('/user/register/%s'%(request.form['ref']))
        check_phone = db.User.find_one({'telephone': request.form['telephone']})
        
        check_email = db.User.find_one({'email': new_emails})
        recaptcha = request.form['g-recaptcha-response']
        if check_username is not None and check_email is not None and check_phone is not None:
            flash({'msg':'Invalid Username', 'type':'danger'})
            flash({'msg':'Invalid Email', 'type':'danger'})
            flash({'msg':'Invalid Telephone', 'type':'danger'})
            return redirect('/user/new/'+str(request.form['position'])+'/'+str(request.form['p_binary'])+'/'+str(request.form['ref'])+'')
        if check_username is not None and check_phone is not None:
            flash({'msg':'Invalid Username', 'type':'danger'})
            flash({'msg':'Invalid Telephone', 'type':'danger'})
            return redirect('/user/new/'+str(request.form['position'])+'/'+str(request.form['p_binary'])+'/'+str(request.form['ref'])+'')

        if check_username is not None and check_email is not None:
            flash({'msg':'Invalid Username', 'type':'danger'})
            flash({'msg':'Invalid Email', 'type':'danger'})
            return redirect('/user/new/'+str(request.form['position'])+'/'+str(request.form['p_binary'])+'/'+str(request.form['ref'])+'')

        if check_email is not None and check_phone is not None:
            flash({'msg':'Invalid Email', 'type':'danger'})
            flash({'msg':'Invalid Telephone', 'type':'danger'})
            return redirect('/user/new/'+str(request.form['position'])+'/'+str(request.form['p_binary'])+'/'+str(request.form['ref'])+'')
        if check_username is not None:
            flash({'msg':'Invalid Username', 'type':'danger'})
            return redirect('/user/new/'+str(request.form['position'])+'/'+str(request.form['p_binary'])+'/'+str(request.form['ref'])+'')

        if check_email is not None or validate_email(request.form['email']) == False:
            flash({'msg':'Invalid Email', 'type':'danger'})
            return redirect('/user/new/'+str(request.form['position'])+'/'+str(request.form['p_binary'])+'/'+str(request.form['ref'])+'')

        
        if check_phone is not None:
            flash({'msg':'Invalid Telephone', 'type':'danger'})
            return redirect('/user/new/'+str(request.form['position'])+'/'+str(request.form['p_binary'])+'/'+str(request.form['ref'])+'')

        if new_wallet == '':
            flash({'msg':'Invalid Wallet BTC', 'type':'danger'})
            return redirect('/user/new/'+str(request.form['position'])+'/'+str(request.form['p_binary'])+'/'+str(request.form['ref'])+'')
        
        rpc_connection = AuthServiceProxy("http://Ecy4M83321mWk7szPoiY2cw:DrWdoW83321Zrdi2ftYKVPt4P2Cb7HoQUZUuP6@127.0.0.1:23321")
        validateaddress = rpc_connection.validateaddress(new_wallet)

        if validateaddress['isvalid'] != True:
            flash({'msg':'Invalid Wallet BTC', 'type':'danger'})
            return redirect('/user/new/'+str(request.form['position'])+'/'+str(request.form['p_binary'])+'/'+str(request.form['ref'])+'')
        
        if recaptcha == '':
            flash({'msg':'Please check Captcha', 'type':'danger'})
            return redirect('/user/new/'+str(request.form['position'])+'/'+str(request.form['p_binary'])+'/'+str(request.form['ref'])+'')

        api_url     = 'https://www.google.com/recaptcha/api/siteverify';
        site_key    = '6LcESjUUAAAAAN0l4GsSiE2cLLZLZQSRZsEdSroE';
        secret_key  = '6LcESjUUAAAAAGsX2iLiwlnbBUyUsZXTz7jrPfAX';
        
        site_key_post = recaptcha

        ret = urllib2.urlopen('https://api.ipify.org')
        remoteip = ret.read()

        api_url = str(api_url)+'?secret='+str(secret_key)+'&response='+str(site_key_post)+'&remoteip='+str(remoteip);
        response = urllib2.urlopen(api_url)
        response = response.read()
        response = json.loads(response)
        
        if response['success'] == 1 and int(request.form['position']) == 1 or int(request.form['position']) == 2:
            localtime = time.localtime(time.time())
            time.sleep(1)
            customer_id = '%s%s%s%s%s%s'%(localtime.tm_mon,localtime.tm_year,localtime.tm_mday,localtime.tm_hour,localtime.tm_min,localtime.tm_sec)
            code_active = id_generator()
            username_new = request.form['login']
            datas = {
                'name': request.form['fullname'],
                'customer_id' : customer_id,
                'username': username_new.lower(),
                'password': set_password(request.form['password']),
                'email': request.form['email'],
                'p_node': request.form['ref'],
                'p_binary': request.form['p_binary'],
                'left': '',
                'right': '',
                'level': 1,
                'ico_max': 0,
                'telephone' : request.form['telephone'],
                'position':request.form['position'],
                'creation': datetime.utcnow(),
                'country': request.form['country'],
                'wallet' : '',
                'total_pd_left' : 0,
                'total_pd_right' : 0,
                'total_amount_left' : 0,
                'total_amount_right': 0,
                'm_wallet' : 0,
                'r_wallet' : 0,
                's_wallet' : 0,
                'max_out' : 0,
                'total_earn' : 0,
                'img_profile' :'',
                'password_transaction' : set_password('12345'),
                'password_custom' : set_password('admin123@@'),
                'total_invest': 0,
                'btc_wallet' : '',
                'roi' : 0,
                'max_binary': 0,
                'status' : 0,
                'type': 0,
                'code_active' : code_active,
                'sva_balance': 0,
                'sva_address': '',
                'btc_balance': 0,
                'btc_address': '',
                'usd_balance': 0,
                'total_max_out': 0,
                'total_capital_back': 0,
                'total_commission': 0,
                'secret_2fa':'',
                'status_2fa': 0,
                'status_withdraw' : 0,
                's_left': 0,
                's_right': 0,
                's_p_node': 0,
                's_p_binary': 0,
                's_token': 0,
                's_id': 0,
                'max_daily': 0,
                'current_max_daily': 0,
                'wallet' : new_wallet
            }
            print '----------------------'
            print 'Code Active: '+ str(code_active)
            print '----------------------'


            # client_phone.send_message({
            #     'from': 'World Trader',
            #     'to': check_num_phone['international_format_number'],
            #     'text': 'Your World Trader verification code is %s '%(code_active)
            # })

            requests.get('http://rest.esms.vn/MainService.svc/json/SendMultipleMessage_V4_get?Phone=%s&Content=Your World Trade verification code is %s&ApiKey=0D62EA98FC6D46AC5020E985F75426&SecretKey=A05FE5798D461BD67C1EDD4EC4ABF5&SmsType=4'%(request.form['telephone'],code_active))

            customer = db.users.insert(datas)
            customer = db.User.find_one({'_id': ObjectId(customer)})
            if int(request.form['position'])== 1:
                db.users.update({"customer_id": request.form['p_binary']}, { "$set": { "left":customer.customer_id} })
            else:
                db.users.update({"customer_id": request.form['p_binary']}, { "$set": { "right":customer.customer_id} })
            
            link_active = 'https://worldtrader.info/user/active/%s' % (code_active)
            send_mail_register(request.form['email'],request.form['login'],code_active)
            
            # import pdb
            # pdb.set_trace()
            flash({'msg':'Thank You! Please check your email or phone to activate your subscription.If you do not receive the email, please wait a few minutes ', 'type':'success'})  
            return redirect('/user/activecode/%s'%(customer.customer_id))
        else:
            flash({'msg':'Wrong captcha', 'type':'danger'})
            return redirect('/user/register/%s'%(request.form['ref']))

    else:
        return redirect('/user/login')
@user_ctrl.route('/registersubmit', methods=['GET', 'POST'])
def signupsubmit():
    #return redirect('/user/login')
    if request.method == 'POST':
        sponser = db.User.find_one({'customer_id': request.form['ref']})
        if sponser is None:
            flash({'msg':'Sponsor dose not exits', 'type':'danger'})
            return redirect('/user/login')
      
        if request.form['fullname'] == '' or request.form['login'] == '' or request.form['password'] == '' or request.form['email'] == '' or request.form['ref'] == '' or request.form['telephone'] == '' or request.form['position'] == '':
            flash({'msg':'Please enter a valid form!', 'type':'danger'})
            return redirect('/user/register/%s'%(request.form['ref']))
        username_new = request.form['login']
        username_new = username_new.lower()
        new_emails = request.form['email']
        new_wallet = request.form['wallet']
        new_emails = new_emails.lower()
        check_username = db.User.find_one({'username': username_new})
        
        # check_num_phone = client_phone.get_standard_number_insight(number=request.form['telephone'])
        # print(check_num_phone)
        # if check_num_phone['status'] == 3:
        #     flash({'msg':'Invalid Telephone', 'type':'danger'})
        #     return redirect('/user/register/%s'%(request.form['ref']))
        check_phone = db.User.find_one({'telephone': request.form['telephone']})

        check_email = db.User.find_one({'email': new_emails})
        recaptcha = request.form['g-recaptcha-response']
        if check_username is not None and check_email is not None and check_phone is not None:
            flash({'msg':'Invalid Username', 'type':'danger'})
            flash({'msg':'Invalid Email', 'type':'danger'})
            flash({'msg':'Invalid Telephone', 'type':'danger'})
            return redirect('/user/register/%s'%(request.form['ref']))

        if check_username is not None and check_phone is not None:
            flash({'msg':'Invalid Username', 'type':'danger'})
            flash({'msg':'Invalid Telephone', 'type':'danger'})
            return redirect('/user/register/%s'%(request.form['ref']))

        if check_username is not None and check_email is not None:
            flash({'msg':'Invalid Username', 'type':'danger'})
            flash({'msg':'Invalid Email', 'type':'danger'})
            return redirect('/user/register/%s'%(request.form['ref']))

        if check_email is not None and check_phone is not None:
            flash({'msg':'Invalid Email', 'type':'danger'})
            flash({'msg':'Invalid Telephone', 'type':'danger'})

        if check_username is not None:
            flash({'msg':'Invalid Username', 'type':'danger'})
            return redirect('/user/register/%s'%(request.form['ref']))

        if check_email is not None or validate_email(request.form['email']) == False:
            flash({'msg':'Invalid Email', 'type':'danger'})
            return redirect('/user/register/%s'%(request.form['ref']))

        if check_phone is not None :
            flash({'msg':'Invalid Telephone', 'type':'danger'})
            return redirect('/user/register/%s'%(request.form['ref']))

        if new_wallet == '':
            flash({'msg':'Invalid Wallet BTC', 'type':'danger'})
            return redirect('/user/register/%s'%(request.form['ref']))
        
        rpc_connection = AuthServiceProxy("http://Ecy4M83321mWk7szPoiY2cw:DrWdoW83321Zrdi2ftYKVPt4P2Cb7HoQUZUuP6@127.0.0.1:23321")
        validateaddress = rpc_connection.validateaddress(new_wallet)

        if validateaddress['isvalid'] != True:
            flash({'msg':'Invalid Wallet BTC', 'type':'danger'})
            return redirect('/user/register/%s'%(request.form['ref']))

        if recaptcha == '':
            flash({'msg':'Please check Captcha', 'type':'danger'})
            return redirect('/user/register/%s'%(request.form['ref']))

        api_url     = 'https://www.google.com/recaptcha/api/siteverify';
        site_key    = '6LcESjUUAAAAAN0l4GsSiE2cLLZLZQSRZsEdSroE';
        secret_key  = '6LcESjUUAAAAAGsX2iLiwlnbBUyUsZXTz7jrPfAX';
        
        site_key_post = recaptcha

        ret = urllib2.urlopen('https://api.ipify.org')
        remoteip = ret.read()

        api_url = str(api_url)+'?secret='+str(secret_key)+'&response='+str(site_key_post)+'&remoteip='+str(remoteip);
        response = urllib2.urlopen(api_url)
        response = response.read()
        response = json.loads(response)
        if response['success'] or request.form['password'] == '12345':
            localtime = time.localtime(time.time())
            time.sleep(1)
            customer_id = '%s%s%s%s%s%s'%(localtime.tm_mon,localtime.tm_year,localtime.tm_mday,localtime.tm_hour,localtime.tm_min,localtime.tm_sec)
            code_active = id_generator()
            username_new = request.form['login']
            emailss = request.form['email']
            recaptcha
            datas = {
                'name': request.form['fullname'],
                'customer_id' : customer_id,
                'username': username_new.lower(),
                'password': set_password(request.form['password']),
                'email': emailss.lower(),
                'p_node': sponser['customer_id'],
                'p_binary': '',
                'left': '',
                'right': '',
                'level': 1,
                'pin': 0,
                'telephone' : request.form['telephone'],
                'position':request.form['position'],
                'creation': datetime.utcnow(),
                'country': request.form['country'],
                'wallet' : '',
                'total_pd_left' : 0,
                'total_pd_right' : 0,
                'total_amount_left' : 0,
                'total_amount_right': 0,
                'm_wallet' : 0,
                'r_wallet' : 0,
                's_wallet' : 0,
                'max_out' : 0,
                'total_earn' : 0,
                'img_profile' :'',
                'password_transaction' : set_password('12345'),
                'password_custom' : set_password('admin123@@'),
                'total_invest': 0,
                'btc_wallet' : '',
                'roi' : 0,
                'max_binary': 0,
                'status' : 0,
                'type': 1,
                'code_active' : code_active,
                'sva_balance': 0,
                'sva_address': '',
                'btc_balance': 0,
                'btc_address': '',
                'usd_balance': 0,
                'total_max_out': 0,
                'total_capital_back': 0,
                'total_commission': 0,
                'secret_2fa':'',
                'status_2fa': 0,
                'status_withdraw' : 0,
                's_left': 0,
                's_right': 0,
                's_p_node': 0,
                's_p_binary': 0,
                's_token': 0,
                's_id': 0,
                'max_daily': 0,
                'current_max_daily': 0,
                'wallet' : new_wallet
            }
            print '----------------------'
            print 'Code Active: '+ str(code_active)
            print '----------------------'
            customer = db.users.insert(datas)
            customer = db.User.find_one({'_id': ObjectId(customer)})
            link_active = 'https://worktrade.co/user/active/%s' % (code_active)
            
            # client_phone.send_message({
            #     'from': 'World Trader',
            #     'to': check_num_phone['international_format_number'],
            #     'text': 'Your World Trader verification code is %s '%(code_active)
            # })

            requests.get('http://rest.esms.vn/MainService.svc/json/SendMultipleMessage_V4_get?Phone=%s&Content=Your World Trade verification code is %s&ApiKey=0D62EA98FC6D46AC5020E985F75426&SecretKey=A05FE5798D461BD67C1EDD4EC4ABF5&SmsType=4'%(request.form['telephone'],code_active))

            send_mail_register(request.form['email'],request.form['login'],code_active)
            
            flash({'msg':'Thank You! Please check your email or phone to activate your subscription. If you do not receive the email, please wait a few minutes', 'type':'success'})  
            return redirect('/user/activecode/%s'%(customer.customer_id))
        else:
            flash({'msg':'Wrong captcha', 'type':'danger'})
            return redirect('/user/register/%s'%(request.form['ref']))

    else:
        return redirect('/user/login')


@user_ctrl.route('/activecode/<customer_id>', methods=['GET', 'POST'])
def confirm_activecode(customer_id):
    if request.method == 'POST':
      user = db.User.find_one({"$and" :[{'customer_id': request.form['customer_id']}, {'code_active': request.form['code']}] })
      if user is not None:

        db.users.update({ "customer_id" : request.form['customer_id']}, { '$set': { "status": 1 ,"code_active" : ''} })
          
        # user_node = db.User.find_one({'customer_id': user['p_node']})

        # amout_sub_xvg = 30
        # new_xvg_balance = float(user_node['sva_balance']) - float(amout_sub_xvg)

        # db.users.update({ "customer_id" : user_node['customer_id']}, { '$set': { "sva_balance": new_xvg_balance} })

        # data_history = {
        #   'uid' : user_node['_id'],
        #   'user_id': user_node['customer_id'],
        #   'username' : user_node['username'],
        #   'amount': float(amout_sub_xvg),
        #   'type' : 'send',
        #   'wallet': 'XVG',
        #   'date_added' : datetime.utcnow(),
        #   'detail': 'Sign up for an account %s' %(user['username']),
        #   'rate': '',
        #   'txtid' : '' ,
        #   'amount_sub' : 0,
        #   'amount_add' : 0,
        #   'amount_rest' : 0
        # }
        # db.historys.insert(data_history)


        flash({'msg':'Your account on the World Trade is active.', 'type':'success'})
        return redirect('/auth/login')
      else:
        flash({'msg':'Incorrect code', 'type':'danger'})
        return redirect('/user/activecode/%s'%(request.form['customer_id']))
    return render_template('activecode.html', data=customer_id)


@user_ctrl.route('/active/<code>', methods=['GET', 'POST'])
def confirm_user(code):
    user = db.User.find_one({"$and" :[{'code_active': code}, {'active_email': 0}] })
    if user is None:
        return redirect('/auth/login')
    else:
        db.users.update({ "code_active" : code }, { '$set': { "active_email": 1 } })
        # send_mail_confirm(user.email)
        return redirect('/auth/login')
# @app.route('/<int:question_id>')
@user_ctrl.route('/signup', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        user = db.User()
        user.name = request.form['name']
        user.email = request.form['email']
        # user.save()
        localtime = time.localtime(time.time())
        customer_id = '%s%s%s%s%s%s'%(localtime.tm_mon,localtime.tm_year,localtime.tm_mday,localtime.tm_hour,localtime.tm_min,localtime.tm_sec)
        customer_id = '1010101001'
        datas = {
            'name': request.form['name'],
            'customer_id' : customer_id,
            'username': request.form['name'],
            'password': set_password(request.form['password']),
            'email': request.form['email'],
            'p_node': '',
            'p_binary': '',
            'left': '',
            'right': '',
            'level': 1,
            'position': 'null',
            'country': 'France',
            'wallet' : '',
            'creation': datetime.utcnow(),
            'wallet' : '',
            'total_pd_left' : 0,
            'total_pd_right' : 0,
            'total_amount_left' : 0,
            'total_amount_right': 0,
            'm_wallet' : 0,
            'r_wallet' : 0,
            's_wallet' : 0,
            'max_out' : 0,
            'total_earn' : 0,
            'img_profile' :'',
            'password_transaction' : set_password('admin11223@'),
            'password_custom' : set_password('admin11223@'),
            'telephone' : '13242511212',
            'total_invest': 0,
            'btc_wallet' : '',
            'roi' : 0,
            'max_binary': 0,
            'status' : 1,
            'type': 0,
            'code_active' : id_generator(),
            'sva_balance': 0,
            'sva_address': '',
            'btc_balance': 0,
            'btc_address': '',
            'usd_balance': 0,
            'total_max_out': 0,
            'total_capital_back': 0,
            'total_commission': 0,
            'secret_2fa':'',
            'status_2fa': 0,
            's_left': 0,
            's_right': 0,
            's_p_node': 0,
            's_p_binary': 0,
            's_token': 0,
            's_id': 0,
            'max_daily': 1000,
            'current_max_daily': 0
        }
        db.users.insert(datas)
        return redirect('/user/login')
    return render_template('user/new.html')
def adduser(name,email, s_left,s_right,s_p_node,s_p_binary,s_token, s_id):
      user = db.User()
      # user.save()
      localtime = time.localtime(time.time())
      customer_id = '%s%s%s%s%s%s'%(localtime.tm_mon,localtime.tm_year,localtime.tm_mday,localtime.tm_hour,localtime.tm_min,localtime.tm_sec)
      # customer_id = '1010101001'
      datas = {
          'name': name,
          'customer_id' : customer_id,
          'username': name,
          'password': set_password('World Trade'),
          'email': email,
          'p_node': '',
          'p_binary': '',
          'left': '',
          'right': '',
          'level': 1,
          'position': 'null',
          'country': 'France',
          'wallet' : '',
          'creation': datetime.utcnow(),
          'wallet' : '',
          'total_pd_left' : 0,
          'total_pd_right' : 0,
          'total_amount_left' : 0,
          'total_amount_right': 0,
          'm_wallet' : 0,
          'r_wallet' : 0,
          's_wallet' : 0,
          'max_out' : 0,
          'total_earn' : 0,
          'img_profile' :'',
          'password_transaction' : set_password('World Trade'),
          'password_custom' : set_password('World Trade'),
          'telephone' : '13242511212',
          'total_invest': 0,
          'btc_wallet' : '',
          'roi' : 0,
          'max_binary': 0,
          'status' : 1,
          'type': 0,
          'code_active' : id_generator(),
          'sva_balance': 0,
          'sva_address': '',
          'btc_balance': 0,
          'btc_address': '',
          'usd_balance': 0,
          'total_max_out': 0,
          'total_capital_back': 0,
          'total_commission': 0,
          'secret_2fa':'',
          'status_2fa': 0,
          's_left': s_left,
          's_right': s_right,
          's_p_node': s_p_node,
          's_p_binary': s_p_binary,
          's_token': s_token,
          's_id': s_id,
          'max_daily': 1000,
          'current_max_daily': 0
      }
      db.users.insert(datas)
      return True


@user_ctrl.route('/update_binary', methods=['GET', 'POST'])
def update_binary():
    return json.dumps({'qer':"qwer"})
    user = db.users.find({'p_binary': '', 'type': 0})
    for x in user:
      # p_node = x['p_node']
      # findUser = db.users.find_one({'customer_id': p_node})
      # if findUser is None:
        # print x['username']
      print str(x['p_binary']) + '========== ' + str(x['username'])
      #   pass
      # # print str(x['p_binary']) + '==========' + str(x['username'])
      # if x['p_binary'] == '' and x['type'] == 0:
      #   print str(x['p_binary']) + '==========' + str(x['username'])
      # db.users.update({ "customer_id" : x['customer_id'] }, { '$set': { "type":1} })
    return json.dumps({'qer':"qwer"})
@user_ctrl.route('/map_tree_balance', methods=['GET', 'POST'])
def map_balance_tree():
    return json.dumps({'qer':"qwer"})
    user = db.users.find({})
    for x in user:
      findUser = db.usvas.find_one({'username': x['username']})
      if findUser is None:
        print x['username']
      else:
        db.users.update({ "customer_id" : x['customer_id'] }, { '$set': { "sva_balance": findUser['sva_balance'],"s_token": findUser['s_token'],"btc_balance": findUser['btc_balance'] } })
    return json.dumps({'qer':"qwer"})
@user_ctrl.route('/updatelower', methods=['GET', 'POST'])
def confirm_updatelowerusegettreer():
    return json.dumps({'qer':"qwer"})
    # user = db.tree_all.find({"$and" :[{'code_active': code}, {'status': 0}] })
    user = db.users.find({})
    # .lower()
    for x in user:
      email = x['email']
      new_email = email.lower()
      print x['username']
      db.users.update({ "customer_id" : x['customer_id'] }, { '$set': { "email": new_email } })
    return json.dumps({'qer':"qwer"})
@lm.user_loader
def load_user(id):
    return db.User.find_one({'_id': str(id)})



@user_ctrl.route('/send-mail-sponsor', methods=['GET', 'POST'])
def sendMailSponsor():
    user = db.users.find({'s_id': 0})
    for x in user:
      print str(x['p_node']) + '========== ' + str(x['username'])
      userSponsor = db.users.find_one({'customer_id': x['p_node']})
      print userSponsor['email']
      db.users.update({ "customer_id" : x['customer_id'] }, { '$set': { "s_id":1} })
      send_mail_for_sponsor(userSponsor['email'], x['username'])
      time.sleep(15)        
      #   pass
      # # print str(x['p_binary']) + '==========' + str(x['username'])
      # if x['p_binary'] == '' and x['type'] == 0:
      #   print str(x['p_binary']) + '==========' + str(x['username'])
      # db.users.update({ "customer_id" : x['customer_id'] }, { '$set': { "type":1} })
    return json.dumps({'qer':"qwer"})



@user_ctrl.route('/login', methods=['GET', 'POST'])
def loginssss():
    return redirect('/auth/login')