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

# from rex.controllers import socket_controller
# app.register_blueprint(blueprint=socket_controller.socket_ctrl, url_prefix='/socket')

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



