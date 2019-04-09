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

from rex.coinpayments import CoinPaymentsAPI
from rex.config import Config
ApiCoinpayment = CoinPaymentsAPI(public_key=Config().public_key,
                          private_key=Config().private_key)

__author__ = 'asdasd'

apiexchange_ctrl = Blueprint('exchange', __name__, static_folder='static', template_folder='templates')
def check_password(pw_hash, password):
        return check_password_hash(pw_hash, password)





@apiexchange_ctrl.route('/submit', methods=['GET', 'POST'])
def submit_exchange():
    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id']
    form = dataDict['form']
    to = dataDict['to']
    amount = dataDict['amount']
    password_transaction = dataDict['password_transaction']

    user = db.User.find_one({'customer_id': customer_id})

    if int(user['security']['email']['status']) == 1:
      if check_password(user['password_transaction'], password_transaction) == True:

        if form == 'BTC':
          val_balance = user['balance']['bitcoin']['available']
        if form == 'ETH':
          val_balance = user['balance']['ethereum']['available']
        if form == 'LTC':
          val_balance = user['balance']['litecoin']['available']
        if form == 'XRP':
          val_balance = user['balance']['ripple']['available']
        if form == 'USDT':
          val_balance = user['balance']['tether']['available']
        if form == 'DASH':
          val_balance = user['balance']['dash']['available']
        if form == 'EOS':
          val_balance = user['balance']['eos']['available']
        if form == 'DOGE':
          val_balance = user['balance']['dogecoin']['available']
        if form == 'BCH':
          val_balance = user['balance']['bitcoincash']['available']
        if form == 'TBT':
          val_balance = user['balance']['coin']['available']

        if float(val_balance) >= float(amount)*100000000:
          if float(user['balance']['coin']['available']) >= 100000:
            ticker = db.tickers.find_one({})

            if form == 'BTC': 
              price_form = ticker['btc_usd']
              string_from = 'balance.bitcoin.available'
              balance_from = user['balance']['bitcoin']['available']
            if form == 'ETH':
              price_form = ticker['eth_usd']
              string_from = 'balance.ethereum.available'
              balance_from = user['balance']['ethereum']['available']
            if form == 'LTC':
              price_form = ticker['ltc_usd']
              string_from = 'balance.litecoin.available'
              balance_from = user['balance']['litecoin']['available']
            if form == 'XRP':
              price_form = ticker['xrp_usd']
              string_from = 'balance.ripple.available'
              balance_from = user['balance']['ripple']['available']
            if form == 'USDT':
              price_form = ticker['usdt_usd']
              string_from = 'balance.tether.available'
              balance_from = user['balance']['tether']['available']
            if form == 'DASH':
              price_form = ticker['dash_usd']
              string_from = 'balance.dash.available'
              balance_from = user['balance']['dash']['available']
            if form == 'EOS':
              price_form = ticker['eso_usd']
              string_from = 'balance.eos.available'
              balance_from = user['balance']['eos']['available']

            if form == 'DOGE':
              price_form = ticker['doge_usd']
              string_from = 'balance.dogecoin.available'
              balance_from = user['balance']['dogecoin']['available']

            if form == 'BCH':
              price_form = ticker['bch_usd']
              string_from = 'balance.bitcoincash.available'
              balance_from = user['balance']['bitcoincash']['available']

            if form == 'TBT':
              price_form = ticker['coin_usd']
              string_from = 'balance.coin.available'
              balance_from = user['balance']['coin']['available']

            amount_usd_form = float(amount)*float(price_form)

            if to == 'BTC': 
              price_to = ticker['btc_usd']
              string_to = 'balance.bitcoin.available'
              balance_to = user['balance']['bitcoin']['available']
            if to == 'ETH':
              price_to = ticker['eth_usd']
              string_to = 'balance.ethereum.available'
              balance_to = user['balance']['ethereum']['available']
            if to == 'LTC':
              price_to = ticker['ltc_usd']
              string_to = 'balance.litecoin.available'
              balance_to = user['balance']['litecoin']['available']
            if to == 'XRP':
              price_to = ticker['xrp_usd']
              string_to = 'balance.ripple.available'
              balance_to = user['balance']['ripple']['available']
            if to == 'USDT':
              price_to = ticker['usdt_usd']
              string_to = 'balance.tether.available'
              balance_to = user['balance']['tether']['available']
            if to == 'DASH':
              price_to = ticker['dash_usd']
              string_to = 'balance.dash.available'
              balance_to = user['balance']['dash']['available']
            if to == 'EOS':
              price_to = ticker['eos_usd']
              string_to = 'balance.eos.available'
              balance_to = user['balance']['eos']['available']

            if to == 'DOGE':
              price_to = ticker['doge_usd']
              string_to = 'balance.dogecoin.available'
              balance_to = user['balance']['dogecoin']['available']
            if to == 'BCH':
              price_to = ticker['bch_usd']
              string_to = 'balance.bitcoincash.available'
              balance_to = user['balance']['bitcoincash']['available']

            if to == 'TBT':
              price_to = ticker['coin_usd']
              string_to = 'balance.coin.available'
              balance_to = user['balance']['coin']['available']

            balance_add = ((float(amount_usd_form)/float(price_to))*100000000)*0.9975
            balance_sub = float(amount)*100000000

            new_balance_add = round((float(balance_add) + float(balance_to)),8)
            new_balance_sub = round((float(balance_from) - float(balance_sub)),8)

            new_coin_fee = round((float(user['balance']['coin']['available']) - 100000),8)

            db.users.update({ "customer_id" : customer_id }, { '$set': { string_from: float(new_balance_sub) ,string_to : float(new_balance_add) } })
            
            #save lich su
            data_history = {
                'uid':  customer_id,
                'user_id': customer_id,
                'username': user['email'],
                'detail':  'exchange',
                'amount_form': round(float(amount),8),
                'amount_to' :  round((float(balance_add)/100000000),8),
                'currency_from' :  form,
                'currency_to' :  to,
                'price_form' : price_form,
                'price_to':  price_to,
                'date_added' : datetime.utcnow()
            }
            db.exchanges.insert(data_history)

            #fee
            userss = db.User.find_one({'customer_id': customer_id})
            new_coin_fee = round((float(userss['balance']['coin']['available']) - 100000),8)
            db.users.update({ "customer_id" : customer_id }, { '$set': { 'balance.coin.available' : new_coin_fee } })
           
            return json.dumps({
                'status': 'complete', 
                'message': 'Account successfully created' 
            })
          else:
            return json.dumps({
                'status': 'error',
                'message': 'You do not have enough 0.001 TBT to make transaction fees' 
            })
        else:
          return json.dumps({
              'status': 'error', 
              'message': 'Your '+str(form)+' balance is not enough to exchange.' 
          })
      else:
        return json.dumps({
          'status': 'error', 
          'message': 'Wrong password transaction. Please try again' 
        })
    else:
      return json.dumps({
        'status': 'error', 
        'message': 'Your account has not been verify.' 
      })
    
@apiexchange_ctrl.route('/submit-support', methods=['GET', 'POST'])
def submit_support():
    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id']
    title = dataDict['title']
    content = dataDict['content']
    user = db.User.find_one({'customer_id': customer_id})
    data_support = {
      'user_id': customer_id,
      'username' : user['email'],
      'message': content,
      'subject': title,
      'reply': [],
      'date_added' : datetime.utcnow(),
      'status': 0
    }
    db.supports.insert(data_support)

    return json.dumps({
        'status': 'complete', 
        'message': 'Account successfully created' 
    })

@apiexchange_ctrl.route('/submit-support-reply', methods=['GET', 'POST'])
def submit_support_reply():
    dataDict = json.loads(request.data)
    _ids = dataDict['_id']
    customer_id = dataDict['customer_id']
    user = db.User.find_one({'customer_id': customer_id})
    content = dataDict['content']
    data_support = {
      'user_id': customer_id,
      'username' : user['email'],
      'message': content,
      'date_added' : datetime.utcnow()
    }
    db.supports.update({ "_id" : ObjectId(_ids) }, { '$set': { "status": 0 }, '$push':{'reply':data_support } })

    return json.dumps({
        'status': 'complete', 
        'message': 'Account successfully created' 
    })
    

@apiexchange_ctrl.route('/get-history', methods=['GET', 'POST'])
def get_historys():

    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id']
    start = dataDict['start']
    limit = dataDict['limit']
    exchanges = db.exchanges.find({'uid': customer_id}).sort([("date_added", -1)]).limit(limit).skip(start)

    #.sort("date_added", -1)

    array = []
    for item in exchanges:
      array.append({
        "username" : item['username'],
        "amount_form" : item['amount_form'],
        "amount_to" : item['amount_to'],
        "price_form" : item['price_form'],
        "price_to" : item['price_to'],
        "currency_from" :  item['currency_from'],
        "currency_to" :  item['currency_to'],
        "date_added" : (item['date_added']).strftime('%H:%M %d-%m-%Y')
      })
    return json.dumps(array)

@apiexchange_ctrl.route('/get-search-history', methods=['GET', 'POST'])
def get_search_history():

    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id']
    from_currency = dataDict['from_currency']
    to_currency = dataDict['to_currency']
    start = dataDict['start']
    limit = dataDict['limit']
    exchanges = db.exchanges.find({'$and' : [{'uid': customer_id},{'currency_from' : from_currency},{'currency_to' : to_currency}]} ).sort([("date_added", -1)]).limit(limit).skip(start)

    array = []
    for item in exchanges:
      array.append({
        "username" : item['username'],
        "amount_form" : item['amount_form'],
        "amount_to" : item['amount_to'],
        "price_form" : item['price_form'],
        "price_to" : item['price_to'],
        "currency_from" :  item['currency_from'],
        "currency_to" :  item['currency_to'],
        "date_added" : (item['date_added']).strftime('%H:%M %d-%m-%Y')
      })
    return json.dumps(array)

@apiexchange_ctrl.route('/get-notification', methods=['GET', 'POST'])
def get_notification():

    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id']
    start = dataDict['start']
    limit = dataDict['limit']
    
    list_notifications = db.notifications.find({'$and' : [{'$or' : [{'uid' : customer_id},{'type' : 'all'}]},{'status' : 0}]} ).sort([("date_added", -1)]).limit(limit).skip(start)

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

@apiexchange_ctrl.route('/count-notification', methods=['GET', 'POST'])
def count_notification():

    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id']
    
    count_notifications = db.notifications.find({'$and' : [{'$or' : [{'uid' : customer_id},{'type' : 'all'}]},{'read' : 0}]} ).count()
    return json.dumps({
      'status' : 'complete',
      'count_notifications' : count_notifications
    })

@apiexchange_ctrl.route('/get-history-transaction', methods=['GET', 'POST'])
def get_history_transaction():

    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id']
    start = dataDict['start']
    limit = dataDict['limit']
    
    history = db.historys.find({'$and' : [{'uid': customer_id}]}).sort([("date_added", -1)]).limit(limit).skip(start)
    #.sort("date_added", -1)

    array = []
    for item in history:
      array.append({
        "username" : item['username'],
        "amount" : item['amount'],
        "currency" : item['currency'],
        "type" : item['type'],
        "detail" : item['detail'],
        "date_added" : (item['date_added']).strftime('%H:%M %d-%m-%Y')
      })
    return json.dumps(array)

@apiexchange_ctrl.route('/get-history-dialing', methods=['GET', 'POST'])
def get_history_dialing():

    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id']
    start = dataDict['start']
    limit = dataDict['limit']
    
    history = db.dialings.find({'$and' : [{'customer_id': customer_id},{'status' : 1}]}).sort([("date_added", -1)]).limit(limit).skip(start)

    array = []
    
    for item in history:
      array.append({
        "username" : item['username'],
        "package" : item['package'],
        "currency" : item['currency'],
        "status" : item['status'],
        "amount_coin" : item['amount_coin'],
        "date_added" : (item['date_added']).strftime('%H:%M %d-%m-%Y')
      })
    return json.dumps(array,)

@apiexchange_ctrl.route('/get-number-dialing', methods=['GET', 'POST'])
def get_number_dialing():

    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id']
    
    history = db.dialings.find({'$and' : [{'customer_id': customer_id}]}).sort([("date_added", -1)])
    #.sort("date_added", -1)

    array = []
    number_dialing = 0
    for item in history:
      if int(item['status']) == 0:
        number_dialing = number_dialing + 1
      
    return json.dumps({
      'number_dialing' : number_dialing
    })

@apiexchange_ctrl.route('/update-number-dialing', methods=['GET', 'POST'])
def update_number_dialing():

    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id']
    number_random = dataDict['number_random']

    history = db.dialings.find_one({'$and' : [{'customer_id': customer_id},{'status' : 0}]})
    #.sort("date_added", -1)
    if history is not None:

      db.dialings.update({'_id': ObjectId(history['_id'])},{'$set' : {'amount_coin' : number_random,'status' :1}})
      customer = db.users.find_one({'customer_id': customer_id})

      coin_balance = float(customer['balance']['coin']['available'])
      new_coin_balance = float(coin_balance) + (float(number_random)*100000000)
      new_coin_balance = float(new_coin_balance)
      db.users.update({ "_id" : ObjectId(customer['_id']) }, { '$set': {'balance.coin.available' : new_coin_balance } })
            
    return json.dumps({
      'status' : 'complete'
    })


@apiexchange_ctrl.route('/get-history-profit', methods=['GET', 'POST'])
def get_history_profit():

    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id']
    types = dataDict['types']
    start = dataDict['start']
    limit = dataDict['limit']
    
    history = db.historys.find({'$and' : [{'uid': customer_id},{'type': types}]}).sort([("date_added", -1)]).limit(limit).skip(start)
    #.sort("date_added", -1)

    array = []
    for item in history:
      array.append({
        "username" : item['username'],
        "amount" : item['amount'],
        "currency" : item['currency'],
        "type" : item['type'],
        "detail" : item['detail'],
        "date_added" : (item['date_added']).strftime('%H:%M %d-%m-%Y')
      })
    return json.dumps(array)


@apiexchange_ctrl.route('/get-history-support', methods=['GET', 'POST'])
def get_history_support():

    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id']
    start = dataDict['start']
    limit = dataDict['limit']
    
    support = db.supports.find({'$and' : [{'user_id': customer_id}]}).sort([("date_added", -1)]).limit(limit).skip(start)
    #.sort("date_added", -1)

    array = []
    for item in support:
      array.append({
        "_id" : str(item['_id']),
        "username" : item['username'],
        "message" : item['message'],
        "subject" : item['subject'],
        "status" : item['status'],
        "date_added" : (item['date_added']).strftime('%H:%M %d-%m-%Y')
      })
    return json.dumps(array)

@apiexchange_ctrl.route('/get-support-id', methods=['GET', 'POST'])
def get_support_id():

    dataDict = json.loads(request.data)
    _ids = dataDict['_id']
    
    item = db.supports.find_one({'_id' :  ObjectId(_ids)})
    reply = []
    for  x in item['reply']  :
      reply.append({
        "username" : (x['username']),
        "message" : x['message'],
        "user_id" : x['user_id'],
        "date_added" : (x['date_added']).strftime('%H:%M %d-%m-%Y')
      })

    return json.dumps({
        "_id" : str(item['_id']),
        "username" : item['username'],
        "message" : item['message'],
        "subject" : item['subject'],
        "status" : item['status'],
        "reply" : reply,
        "date_added" : (item['date_added']).strftime('%H:%M %d-%m-%Y')
      })

@apiexchange_ctrl.route('/get-notification-id', methods=['GET', 'POST'])
def get_notification_id():

    dataDict = json.loads(request.data)
    _ids = dataDict['_id']
    
    item = db.notifications.find_one({'_id' :  ObjectId(_ids)})
    db.notifications.update({ "_id" : ObjectId(_ids) }, { '$set': { 'read': 1} })

    return json.dumps({
      "_id" : str(item['_id']),
      "username" : item['username'],
      "content" : item['content'],
      "date_added" : (item['date_added']).strftime('%H:%M %d-%m-%Y')
    })



    
@apiexchange_ctrl.route('/get-member', methods=['GET', 'POST'])
def get_member():

    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id']
    start = dataDict['start']
    limit = dataDict['limit']
    member = db.users.find({'p_node': customer_id}).sort([("creation", -1)]).limit(limit).skip(start)

    #.sort("date_added", -1)

    array = []
    for item in member:
      array.append({
        "customer_id" : item['customer_id'],
        "email" : item['email'],
        "level" : item['level'],
        "img_profile" : item['personal_info']['img_profile'],
        "date_added" : (item['creation']).strftime('%H:%M %d-%m-%Y')
      })
    return json.dumps(array)

@apiexchange_ctrl.route('/get-infomation-user', methods=['GET', 'POST'])
def get_infomation_user():

    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id']
    
    user = db.users.find_one({'customer_id': customer_id})
    if user is not None:
      return json.dumps({
          'status': 'complete', 
          'email': user['email'],
          'date_added' : (user['creation']).strftime('%H:%M %d-%m-%Y'),
          'investment': user['investment'],
          'img_profile' : user['img_profile'],
          'img_address' : user['personal_info']['img_address'],
          'img_passport_fontside' : user['personal_info']['img_passport_fontside'],
          'img_passport_backside' : user['personal_info']['img_passport_backside'],
          'telephone' : user['telephone'],
          'firstname' : user['personal_info']['firstname'],
          'address' : user['personal_info']['address'],
          'lastname' : user['personal_info']['lastname'],
          'date_birthday' : user['personal_info']['date_birthday'],
          'verification' : user['verification'],
          'd_wallet' : user['d_wallet'],
          'r_wallet' : user['r_wallet'],
          's_wallet' : user['s_wallet'],
          'l_wallet' : user['l_wallet'],
          'ss_wallet' : user['ss_wallet'],
          'sf_wallet' : user['sf_wallet']
      })
    else:
      return json.dumps({
          'status': 'error'
      })
   
