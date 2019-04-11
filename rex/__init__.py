from json import dumps
import json
from flask import Flask, send_from_directory, send_file, Blueprint, jsonify,session, request, redirect, url_for, render_template, json, flash, send_file
from flask.ext.login import login_required, LoginManager, current_user
from flask.ext.mongokit import MongoKit
from flask.templating import render_template
import os
import settings
from random import randint
from hashlib import sha256
import string
import random
from datetime import datetime
from datetime import datetime, date, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO
import requests
import json
from flask_socketio import emit
from bson.objectid import ObjectId
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

# from flask_recaptcha import ReCaptcha
__author__ = 'carlozamagni'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config.from_object(settings)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# socketio = SocketIO()
# socketio.init_app(app)

db = MongoKit(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = '/auth/login'

from rex.controllers import api_controller
app.register_blueprint(blueprint=api_controller.api_ctrl, url_prefix='/api')
from rex.controllers import apideposit_controller
app.register_blueprint(blueprint=apideposit_controller.apidepist_ctrl, url_prefix='/api/deposit')
from rex.controllers import apiexchange_controller
app.register_blueprint(blueprint=apiexchange_controller.apiexchange_ctrl, url_prefix='/api/exchange')
from rex.controllers import apiinvestment_controller
app.register_blueprint(blueprint=apiinvestment_controller.apiinvestment_ctrl, url_prefix='/api/investment')

from rex.controllers import admin_controller
app.register_blueprint(blueprint=admin_controller.admin_ctrl, url_prefix='/admin')
from rex.controllers import admin
app.register_blueprint(blueprint=admin.admin1_ctrl, url_prefix='/admin')



@app.route('/api/update-price') 
def function():
    

    url = 'https://min-api.cryptocompare.com/data/price?fsym=USD&tsyms=BTC,ETH,LTC,BCH'
    r = requests.get(url)
    response_dict = r.json()

     
    data_ticker = db.tickers.find_one({})
    data_ticker['btc_usd'] = round(1/float(response_dict['BTC']),2)
    data_ticker['bch_usd'] = round(1/float(response_dict['BCH']),2)
    data_ticker['ltc_usd'] = round(1/float(response_dict['LTC']),2)
    data_ticker['eth_usd'] = round(1/float(response_dict['ETH']),2)
   
    db.tickers.save(data_ticker)
    return json.dumps({'status': 'success'})



@app.template_filter()
def format_int(value): # date = datetime object.
    return int(value)

@app.template_filter()
def format_date(date): # date = datetime object.
    return date.strftime('%Y-%m-%d %H:%M:%S')
@app.template_filter()
def format_only_date(date): # date = datetime object.
    return date.strftime('%Y-%m-%d')
@app.template_filter()
def find_username(uid): # date = datetime object.
    if uid:
        uid = uid
    else:
        uid ='1111111'
    user = db.User.find_one({'customer_id': uid})
    if user is None:
        return ''
    else:
        return user.username

@app.template_filter()
def find_user_usd(uid): # date = datetime object.
    if uid:
        uid = str(uid)
    else:
        uid ='1111111'
    user = db.users.find_one({'_id': ObjectId(uid)})
    if user is None:
        return ''
    else:
        return user['usd_balance']

@app.template_filter()
def find_user_sva(uid): # date = datetime object.
    if uid:
        uid = uid
    else:
        uid ='1111111'
    user = db.users.find_one({'_id': ObjectId(uid)})
    if user is None:
        return ''
    else:
        return user['sva_balance']

@app.template_filter()
def to_string(value):
    
    return str(value)
@app.template_filter()
def number_format(value, tsep=',', dsep='.'):
    s = unicode(value)
    cnt = 0
    numchars = dsep + '0123456789'
    ls = len(s)
    while cnt < ls and s[cnt] not in numchars:
        cnt += 1

    lhs = s[:cnt]
    s = s[cnt:]
    if not dsep:
        cnt = -1
    else:
        cnt = s.rfind(dsep)
    if cnt > 0:
        rhs = dsep + s[cnt+1:]
        s = s[:cnt]
    else:
        rhs = ''

    splt = ''
    while s != '':
        splt = s[-3:] + tsep + splt
        s = s[:-3]

    return lhs + splt[:-1] + rhs
@app.template_filter()
def format_round(value):
    value = float(value)
    return '{:20,.8f}'.format(value)
@app.template_filter()
def format_usd(value):
    value = float(value)
    return '{:20,.2f}'.format(value)

@app.template_filter()
def format_satoshi(value):
    value = float(value)
    return '{:.8f}'.format(value)

@app.template_filter()
def format_btc_usd(value):
    data_ticker = db.tickers.find_one({})
    btc_usd = data_ticker['btc_usd']
    value = float(value)*float(btc_usd)
    return '{:20,.2f}'.format(value)

@app.template_filter()
def format_xvg_usd(value):
    data_ticker = db.tickers.find_one({})
    xvg_usd = data_ticker['xvg_usd']
    value = float(value)*0.8
    return '{:20,.2f}'.format(value)


@app.template_filter()
def format_usds(value):
    value = float(value)
    return '{:20,.0f}'.format(value)

@app.template_filter()
def format_altcoin(value):
    value = float(value)/100000000
    return '{:20,.8f}'.format(value)

@app.template_filter()
def format_html(html):
    return html



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def set_password(password):
    return generate_password_hash(password)
@app.route('/setup')
def setup():
    inserted = []
    #return json.dumps({'status' : 'error'})
    profit = [{"_id" : "5995a569587b3b15a14174e0",
        '500': 0.1,
        '1000':  0.2,
        '3000' : 0.3,
        '5000' : 0.4,
        '10000' : 0.5,
        '30000' : 0.6,
        '50000': 0.7,
        '100000':  0.8,
        '500000' : 0.9,
        '1000000' : 1
    }]
    db['profits'].drop()
    db['profits'].insert(profit)
    
    # users = [{"_id" : "5995a569587b3b15a14174e0",
    # "roi" : 100920,
    # "right" : "",
    # "p_binary" : "",
    # "m_wallet" : 600000000,
    # "creation" : datetime.utcnow(),
    # "telephone" : "000000000",
    # "password_transaction" : set_password('12345'),
    # "total_amount_right" : int("0"),
    # "total_pd_right" : int("0"),
    # "btc_wallet" : "19WpQavvcEcy4MmWk7szPoiY2cwvi8jt9E",
    # "p_node" : "",
    # "r_wallet" : 600000000,
    # "password_custom" : set_password('12345'),
    # "total_pd_left" : 9700,
    # "customer_id" : "1010101001",
    # "email" : "meccafunds@meccafund.org",
    # "total_amount_left" : 10500,
    # "username" : "root",
    # "s_wallet" : 1000000000,
    # "total_invest" : 100000,
    # "password" : set_password('12345'),
    # "img_profile" : "",
    # "max_out" : 500000,
    # "max_binary" : 500000,
    # "name" : "MECCAFUND",
    # "level" : int("3"),
    # "country" : "French Southern territories",
    # "wallet" : "",
    # "status" : 1,
    # "total_earn" : 10000,
    # "position" : "",
    # 'sva_balance': 0,
    # 'sva_address': '',
    # 'btc_balance': 0,
    # 'btc_address': '',
    # 'usd_balance': 0,
    # 'total_max_out': 0,
    # 'total_capital_back': 0,
    # 'total_commission': 0,
    # 'secret_2fa':'',
    # 'status_2fa': 0,
    # "left" : "",
    # 's_left': 0,
    # 's_right': 0,
    # 's_p_node': 0,
    # 's_p_binary': 0,
    # 's_token': 0,
    # 's_id': 0
    # }]
    # db['users'].drop()
    # db['users'].insert(users)
    # inserted.append(users)

    # admin = [{
    #     "_id" : "1175a9437u2b3b15a14174e0",
    #     'username':  'admin',
    #     'email' :  'admin@admin.com',
    #     'password': set_password('12345'),
    #     'sum_withdraw': 0,
    #     'sum_invest' : 0
    # }]
    # db['admins'].drop()
    # db['admins'].insert(admin)
    # inserted.append(admin)

    # ticker = [{
    #     'btc_usd' : 7500,
    #     'sva_btc' : 0.00013333,
    #     'sva_usd' : 1
    # }]
    # db['tickers'].drop()
    # db['tickers'].insert(ticker)

    return json.dumps(inserted)
   


@app.route('/')
def home_page():
    data ={
    'menu' : 'home'
    }
    return render_template('home/index.html', data=data)

@app.route('/privacy-policy.aspx')
def howitworks():
    data ={
    'menu' : 'home'
    }
    return render_template('home/privacy-policy.html', data=data)

# @app.route('/about.aspx')
# def about():
#     data ={
#     'menu' : 'home'
#     }
#     return render_template('home/about.html', data=data)

# @app.route('/srilanka.aspx')
# def srilanka():
#     data ={
#     'menu' : 'home'
#     }
#     return render_template('home/srilanka.html', data=data)
# @app.route('/singapore.aspx')
# def singapore():
#     data ={
#     'menu' : 'home'
#     }
#     return render_template('home/singapore.html', data=data)
# @app.route('/dubai.aspx')
# def dubai():
#     data ={
#     'menu' : 'home'
#     }
#     return render_template('home/dubai.html', data=data)
# @app.route('/other.aspx')
# def other():
#     data ={
#     'menu' : 'home'
#     }
#     return render_template('home/other.html', data=data)
# @app.route('/investment.aspx')
# def investment():
#     data ={
#     'menu' : 'home'
#     }
#     return render_template('home/investment.html', data=data)
# @app.route('/blog.aspx')
# def blog():
#     data ={
#     'menu' : 'home'
#     }
#     return render_template('home/blog.html', data=data)
# @app.route('/contact.aspx')
# def contact():
#     data ={
#     'menu' : 'home'
#     }
#     return render_template('home/contact.html', data=data)
