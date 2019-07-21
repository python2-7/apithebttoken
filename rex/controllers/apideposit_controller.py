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
rpc_connection = AuthServiceProxy(Config().rpc_connection)
sys.setrecursionlimit(10000)
digits58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

from rex.coinpayments import CoinPaymentsAPI

ApiCoinpayment = CoinPaymentsAPI(public_key=Config().public_key,
                          private_key=Config().private_key)

__author__ = 'asdasd'

apidepist_ctrl = Blueprint('deposit', __name__, static_folder='static', template_folder='templates')
def check_password(pw_hash, password):
        return check_password_hash(pw_hash, password)

def id_generator(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@apidepist_ctrl.route('/get-address', methods=['GET', 'POST'])
def get_address():
    dataDict = json.loads(request.data)
    
    customer_id = dataDict['customer_id']
    currency = dataDict['currency']
    

    url_callback = 'http://192.254.73.26:51029/api/deposit/jskfkjsfhkjsdhfqwtryqweqeweqeqwe'
    user = db.users.find_one({'customer_id': customer_id})
    if currency == 'BTC':
      if user['balance']['bitcoin']['cryptoaddress'] == '':
        respon_wallet_btc = ApiCoinpayment.get_callback_address(currency='BTC', ipn_url=url_callback)
        if respon_wallet_btc['error'] == 'ok':
          new_wallet =  respon_wallet_btc['result']['address']
          if len(new_wallet.split("coinpaymt")) > 1:
            new_wallet = ''
          db.users.update({ "customer_id" : customer_id }, { '$set': { "balance.bitcoin.cryptoaddress": new_wallet } })
        else:
          new_wallet = ''
      else:
        new_wallet = user['balance']['bitcoin']['cryptoaddress']

    if currency == 'ETH':
      if user['balance']['ethereum']['cryptoaddress'] == '':
        respon_wallet_btc = ApiCoinpayment.get_callback_address(currency='ETH', ipn_url=url_callback)
        if respon_wallet_btc['error'] == 'ok':
          new_wallet =  respon_wallet_btc['result']['address']
          if len(new_wallet.split("coinpaymt")) > 1:
            new_wallet = ''
          db.users.update({ "customer_id" : customer_id }, { '$set': { "balance.ethereum.cryptoaddress": new_wallet } })
        else:
          new_wallet = ''
      else:
        new_wallet = user['balance']['ethereum']['cryptoaddress']

    if currency == 'LTC':
      if user['balance']['litecoin']['cryptoaddress'] == '':
        respon_wallet_btc = ApiCoinpayment.get_callback_address(currency='LTC', ipn_url=url_callback)
        if respon_wallet_btc['error'] == 'ok':
          new_wallet =  respon_wallet_btc['result']['address']
          if len(new_wallet.split("coinpaymt")) > 1:
            new_wallet = ''
          db.users.update({ "customer_id" : customer_id }, { '$set': { "balance.litecoin.cryptoaddress": new_wallet } })
        else:
          new_wallet = ''
      else:
        new_wallet = user['balance']['litecoin']['cryptoaddress']


    if currency == 'XRP':
      if user['balance']['ripple']['cryptoaddress'] == '':
        respon_wallet_btc = ApiCoinpayment.get_callback_address(currency='XRP', ipn_url=url_callback)
        if respon_wallet_btc['error'] == 'ok':
          new_wallet =  respon_wallet_btc['result']['address']
          if len(new_wallet.split("coinpaymt")) > 1:
            new_wallet = ''
          db.users.update({ "customer_id" : customer_id }, { '$set': { "balance.ripple.cryptoaddress": new_wallet } })
        else:
          new_wallet = ''
      else:
        new_wallet = user['balance']['ripple']['cryptoaddress']

    if currency == 'USDT':
      if user['balance']['tether']['cryptoaddress'] == '':
        respon_wallet_btc = ApiCoinpayment.get_callback_address(currency='USDT', ipn_url=url_callback)
        if respon_wallet_btc['error'] == 'ok':
          new_wallet =  respon_wallet_btc['result']['address']
          if len(new_wallet.split("coinpaymt")) > 1:
            new_wallet = ''
          db.users.update({ "customer_id" : customer_id }, { '$set': { "balance.tether.cryptoaddress": new_wallet } })
        else:
          new_wallet = ''
      else:
        new_wallet = user['balance']['tether']['cryptoaddress']


    if currency == 'EOS':
      if user['balance']['eos']['cryptoaddress'] == '':
        respon_wallet_btc = ApiCoinpayment.get_callback_address(currency='EOS', ipn_url=url_callback)
        if respon_wallet_btc['error'] == 'ok':
          new_wallet =  respon_wallet_btc['result']['address']
          if len(new_wallet.split("coinpaymt")) > 1:
            new_wallet = ''
          db.users.update({ "customer_id" : customer_id }, { '$set': { "balance.eos.cryptoaddress": new_wallet } })
        else:
          new_wallet = ''
      else:
        new_wallet = user['balance']['eos']['cryptoaddress']

    if currency == 'DASH':
      if user['balance']['dash']['cryptoaddress'] == '':
        respon_wallet_btc = ApiCoinpayment.get_callback_address(currency='DASH', ipn_url=url_callback)
        if respon_wallet_btc['error'] == 'ok':
          new_wallet =  respon_wallet_btc['result']['address']
          if len(new_wallet.split("coinpaymt")) > 1:
            new_wallet = ''
          db.users.update({ "customer_id" : customer_id }, { '$set': { "balance.dash.cryptoaddress": new_wallet } })
        else:
          new_wallet = ''
      else:
        new_wallet = user['balance']['dash']['cryptoaddress']

    if currency == 'DOGE':
      if user['balance']['dogecoin']['cryptoaddress'] == '':
        respon_wallet_btc = ApiCoinpayment.get_callback_address(currency='DOGE', ipn_url=url_callback)
        if respon_wallet_btc['error'] == 'ok':
          new_wallet =  respon_wallet_btc['result']['address']
          if len(new_wallet.split("coinpaymt")) > 1:
            new_wallet = ''
          db.users.update({ "customer_id" : customer_id }, { '$set': { "balance.dogecoin.cryptoaddress": new_wallet } })
        else:
          new_wallet = ''
      else:
        new_wallet = user['balance']['dogecoin']['cryptoaddress']

    if currency == 'BCH':
      if user['balance']['bitcoincash']['cryptoaddress'] == '':
        respon_wallet_btc = ApiCoinpayment.get_callback_address(currency='BCH', ipn_url=url_callback)
        if respon_wallet_btc['error'] == 'ok':
          new_wallet =  respon_wallet_btc['result']['address']
          if len(new_wallet.split("coinpaymt")) > 1:
            new_wallet = ''
          db.users.update({ "customer_id" : customer_id }, { '$set': { "balance.bitcoincash.cryptoaddress": new_wallet } })
        else:
          new_wallet = ''
      else:
        new_wallet = user['balance']['bitcoincash']['cryptoaddress']

    if currency == 'TBT':
      if user['balance']['coin']['cryptoaddress'] == '':
        new_wallet = rpc_connection.getnewaddress('')
        if new_wallet:
          db.users.update({ "customer_id" : customer_id }, { '$set': { "balance.coin.cryptoaddress": new_wallet } })
        else:
          new_wallet = ''
      else:
        new_wallet = user['balance']['coin']['cryptoaddress']
    
    
    if len(new_wallet.split("coinpaymt")) > 1 or new_wallet == '':
        return json.dumps({
            'status': 'error', 
            'message': 'The system is maintenance. Please come back later.' 
        })

    return json.dumps({
        'status': 'complete', 
        'address': new_wallet 
    })

@apidepist_ctrl.route('/jskfkjsfhkjsdhfqwtryqweqeweqeqwe', methods=['GET', 'POST'])
def CallbackCoinPayment():
  print "callback"
  print request.form
  if request.method == 'POST':
    tx = request.form['txn_id'];
    address = request.form['address'];
    amount = request.form['amount'];
    currency = request.form['currency'];

    ticker = db.tickers.find_one({})

    if currency == 'BTC':
      query_search = {'balance.bitcoin.cryptoaddress' : address}
      price = ticker['btc_usd']
    if currency == 'ETH':
      query_search = {'balance.ethereum.cryptoaddress' : address}
      price = ticker['eth_usd']
    if currency == 'USDT':
      query_search = {'balance.tether.cryptoaddress' : address}
      price = ticker['usdt_usd']
    if currency == 'XRP':
      query_search = {'balance.ripple.cryptoaddress' : address}
      price = ticker['xrp_usd']
    if currency == 'LTC':
      query_search = {'balance.litecoin.cryptoaddress' : address}
      price = ticker['ltc_usd']
    if currency == 'EOS':
      query_search = {'balance.eos.cryptoaddress' : address}
      price = ticker['eos_usd']
    if currency == 'BCH':
      query_search = {'balance.bitcoincash.cryptoaddress' : address}
      price = ticker['bch_usd']
    if currency == 'DOGE':
      query_search = {'balance.dogecoin.cryptoaddress' : address}
      price = ticker['doge_usd']
    if currency == 'DASH':
      query_search = {'balance.dash.cryptoaddress' : address}
      price = ticker['dash_usd']
      
    check_wallet = db.wallets.find_one({'$and' : [{'txt_id': tx},{'type' : 'deposit'}]} )
    customer = db.users.find_one(query_search)

    if check_wallet is None and customer is not None:
      
      data = {
        'user_id': customer['_id'],
        'uid': customer['customer_id'],
        'username': customer['username'],
        'amount': amount,
        'type': 'deposit',
        'txt_id': tx,
        'date_added' : datetime.utcnow(),
        'status': 1,
        'address': address,
        'currency' : currency,
        'confirmations' : 0,
        'amount_usd': float(price) * float(amount),
        'price' : price,
      }
      db.wallets.insert(data)
      if currency == 'BTC':
        new_balance_wallets = float(customer['balance']['bitcoin']['available']) + float(amount)*100000000
        db.users.update(query_search, { '$set': { "balance.bitcoin.available": float(new_balance_wallets) } })

      if currency == 'ETH':
        new_balance_wallets = float(customer['balance']['ethereum']['available']) + float(amount)*100000000
        db.users.update(query_search, { '$set': { "balance.ethereum.available": float(new_balance_wallets) } })

      if currency == 'LTC':
        new_balance_wallets = float(customer['balance']['litecoin']['available']) + float(amount)*100000000
        db.users.update(query_search, { '$set': { "balance.litecoin.available": float(new_balance_wallets) } })

      if currency == 'XRP':
        new_balance_wallets = float(customer['balance']['ripple']['available']) + float(amount)*100000000
        db.users.update(query_search, { '$set': { "balance.ripple.available": float(new_balance_wallets) } })

      if currency == 'USDT':
        new_balance_wallets = float(customer['balance']['tether']['available']) + float(amount)*100000000
        db.users.update(query_search, { '$set': { "balance.tether.available": float(new_balance_wallets) } })
      
      if currency == 'EOS':
        new_balance_wallets = float(customer['balance']['eos']['available']) + float(amount)*100000000
        db.users.update(query_search, { '$set': { "balance.eos.available": float(new_balance_wallets) } })
      
      if currency == 'DASH':
        new_balance_wallets = float(customer['balance']['dash']['available']) + float(amount)*100000000
        db.users.update(query_search, { '$set': { "balance.dash.available": float(new_balance_wallets) } })

      if currency == 'BCH':
        new_balance_wallets = float(customer['balance']['bitcoincash']['available']) + float(amount)*100000000
        db.users.update(query_search, { '$set': { "balance.bitcoincash.available": float(new_balance_wallets) } })

      if currency == 'DOGE':
        new_balance_wallets = float(customer['balance']['dogecoin']['available']) + float(amount)*100000000
        db.users.update(query_search, { '$set': { "balance.dogecoin.available": float(new_balance_wallets) } })
      
  return json.dumps({'txid': 'complete'})

@apidepist_ctrl.route('/callbackcoin/jskfkjsfhkjsdhfqwtryqweqeweqeqwe/<txid>', methods=['GET', 'POST'])
def callbackcoin(txid):
    transaction = rpc_connection.gettransaction(txid)
    if transaction:
      print transaction
      confirmations = transaction['confirmations']
      check_wallet = db.wallets.find_one({'$and' : [{'txt_id': txid},{'type' : 'deposit'},{'currency' : 'TBT'}]} )
      if check_wallet is None:
        details = transaction['details']
        if len(details) > 0:
          ticker = db.tickers.find_one({})
          for x in details:
            if x['category'] == 'receive':
              address = x['address']
              amount = float(x['amount'])
              customer = db.users.find_one({'balance.coin.cryptoaddress' : address})
              if customer:
                data = {
                  'user_id': customer['_id'],
                  'uid': customer['customer_id'],
                  'username': customer['username'],
                  'amount': amount,
                  'type': 'deposit',
                  'txt_id': txid,
                  'date_added' : datetime.utcnow(),
                  'status': 1,
                  'address': address,
                  'currency' : 'TBT',
                  'confirmations' : confirmations,
                  'amount_usd': float(ticker['coin_usd']) * float(amount),
                  'price' : ticker['coin_usd'],
                }
                db.wallets.insert(data)
                new_balance_wallets = float(customer['balance']['coin']['available']) + float(amount)*100000000
                db.users.update({'balance.coin.cryptoaddress' : address}, { '$set': { "balance.coin.available": float(new_balance_wallets) } })
              
    return json.dumps({'txid': txid})
@apidepist_ctrl.route('/get-history-currency', methods=['GET', 'POST'])
def get_history_currency():
    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id']
    currency = dataDict['currency']
    start = dataDict['start']
    limit = dataDict['limit']
    list_wallet = db.wallets.find({'$and' : [{'uid': customer_id},{'currency': currency}, {'$or' : [{'status': 1},{'status': 0}]} ]}).sort([("date_added", -1)]).limit(limit).skip(start)
    array = []
    for item in list_wallet:
      
      array.append({
        "username" : item['username'],
        "status" : item['status'],
        "amount" : item['amount'],
        "txt_id" : item['txt_id'],
        "address" : item['address'],
        "date_added" : (item['date_added']).strftime('%H:%M %d-%m-%Y'),
        "type" : item['type'],
        "currency" : item['currency'],
        "confirmations" : item['confirmations'],
        "amount_usd" : item['amount_usd'],
        "price" : item['price']
      })

    return json.dumps(array)
    
@apidepist_ctrl.route('/add-wallet-address', methods=['GET', 'POST'])
def add_wallet_address():
    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id']
    name = dataDict['name']
    address = dataDict['address']
    currency = dataDict['currency']
    password_transaction = dataDict['password_transaction'].lower()

    customer = db.users.find_one({'customer_id' : customer_id})

    check_name = db.contacts.find_one({'$and' : [{'customer_id' : customer_id},{'name': name},{'currency': currency}]})
    check_address = db.contacts.find_one({'$and' : [{'customer_id' : customer_id},{'address': address},{'currency': currency}]})
    if check_name is None:
        if check_address is None:
            if check_password(customer['password_transaction'], password_transaction) == True:
                url_api = "http://192.254.73.26:59888/crypto-address-validator?wallet="+address+"&currency="+currency+""
                r = requests.get(url_api)
                response_dict = r.json()
                if response_dict['message'] == True:
                    data = {
                        'uid': customer['customer_id'],
                        'username': customer['username'],
                        'name': name,
                        'address':  address,
                        'currency': currency,
                        'date_added' : datetime.utcnow(),
                        'status': 0
                      }
                    db.contacts.insert(data)
                    return json.dumps({
                      'status': 'complete', 
                      'message': 'Add success' 
                    })
                else:
                    return json.dumps({
                      'status': 'error', 
                      'message': 'The wrong address. Please try again' 
                    })
            else:
                return json.dumps({
                  'status': 'error', 
                  'message': 'Wrong password transaction. Please try again' 
                })
        else:
            return json.dumps({
              'status': 'error', 
              'message': 'Address already exists. Please try again' 
            })
    else:
        return json.dumps({
          'status': 'error', 
          'message': 'Name already exists. Please try again' 
        })
            
@apidepist_ctrl.route('/get-contact-currency', methods=['GET', 'POST'])
def get_contact_currency():

    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id']
    currency = dataDict['currency']
    
    contact = db.contacts.find({'$and' : [{'uid': customer_id},{'currency' : currency}]}).sort([("date_added", -1)])

    array = []
    for item in contact:
      array.append({
        'uid': item['uid'],
        'username': item['username'],
        'name': item['name'],
        'address':  item['address'],
        'currency': item['currency'],
        'date_added' : (item['date_added']).strftime('%H:%M %d-%m-%Y'),
        'status': item['status']
      })
    return json.dumps(array)


@apidepist_ctrl.route('/withdraw-currency', methods=['GET', 'POST'])
def withdraw_currency():
    
    if int(date.weekday(date.today())) != 0: 
      return json.dumps({
          'status': 'error',
          'message': 'Withdraw on every Monday.' 
      })
    else:

      dataDict = json.loads(request.data)
      customer_id = dataDict['customer_id']
      currency = dataDict['currency']
      amount = dataDict['amount']
      address = dataDict['address']
      password_transaction = dataDict['password_transaction'].lower()

      user = db.User.find_one({'customer_id': customer_id})

      if user is not None:
        if int(user['security']['email']['status']) == 1:

          ticker = db.tickers.find_one({})
          if currency == 'BTC':
            val_balance = user['balance']['bitcoin']['available']
            price_atlcoin = ticker['btc_usd']
            string_query = 'balance.bitcoin.available'
            min_withdraw = 0.002
          if currency == 'ETH':
            val_balance = user['balance']['ethereum']['available']
            price_atlcoin = ticker['eth_usd']
            string_query = 'balance.ethereum.available'
            min_withdraw = 0.02
          if currency == 'LTC':
            val_balance = user['balance']['litecoin']['available']
            price_atlcoin = ticker['ltc_usd']
            string_query = 'balance.litecoin.available'
            min_withdraw = 0.002
          if currency == 'XRP':
            val_balance = user['balance']['ripple']['available']
            price_atlcoin = ticker['xrp_usd']
            string_query = 'balance.ripple.available'
            min_withdraw = 22
          if currency == 'USDT':
            val_balance = user['balance']['tether']['available']
            price_atlcoin = ticker['usdt_usd']
            string_query = 'balance.tether.available'
            min_withdraw = 6.6
          if currency == 'DASH':
            val_balance = user['balance']['dash']['available']
            price_atlcoin = ticker['dash_usd']
            string_query = 'balance.dash.available'
            min_withdraw = 0.004
          if currency == 'EOS':
            val_balance = user['balance']['eos']['available']
            price_atlcoin = ticker['eos_usd']
            string_query = 'balance.eos.available'
            min_withdraw = 0.2
          if currency == 'BCH':
            val_balance = user['balance']['bch']['available']
            price_atlcoin = ticker['bch_usd']
            string_query = 'balance.bch.available'
            min_withdraw = 0.2
          if currency == 'TBT':
            val_balance = user['balance']['coin']['available']
            price_atlcoin = ticker['coin_usd']
            string_query = 'balance.coin.available'
            min_withdraw = 0.1

          if float(amount) > min_withdraw:

              if check_password(user['password_transaction'], password_transaction) == True:
                  
                  if float(val_balance) >= (float(amount)*100000000):
                    
                    if float(user['balance']['coin']['available']) >= 100000:

                      url_api = "http://192.254.73.26:59888/crypto-address-validator?wallet="+address+"&currency="+currency+""
                      
                      r = requests.get(url_api)
                      response_dict = r.json()
                      if response_dict['message'] == True:
                        
                        code_active = id_generator(20)

                        data = {
                          'user_id': user['_id'],
                          'uid': user['customer_id'],
                          'username': user['username'],
                          'amount': float(amount),
                          'date_added' : datetime.utcnow(),
                          'status': 0,
                          'address': address,
                          'currency' : currency,
                          'code_active' : code_active,
                          'active_email' : 0,
                          'amount_usd': float(price_atlcoin) * float(amount),
                          'price' : price_atlcoin
                        }
                        db.withdraws.insert(data)
                        send_mail_withdraw_user(user['email'],amount,currency,address,code_active)
                        # amount_usd = float(amount)*float(price_atlcoin)
                        
                        # new_balance_sub = round(float(val_balance) - (float(amount)*100000000),8)

                        # db.users.update({ "customer_id" : customer_id }, { '$set': { string_query: float(new_balance_sub) } })
                        
                        # #save lich su
                        # data = {
                        #   'user_id': user['_id'],
                        #   'uid': user['customer_id'],
                        #   'username': user['username'],
                        #   'amount': float(amount),
                        #   'type': 'withdraw',
                        #   'txt_id': 'Pending',
                        #   'date_added' : datetime.utcnow(),
                        #   'status': 0,
                        #   'address': address,
                        #   'currency' : currency,
                        #   'confirmations' : 0,
                        #   'amount_usd': float(price_atlcoin) * float(amount),
                        #   'price' : price_atlcoin,
                        #   'id_coinpayment' : ''
                        # }
                        # db.wallets.insert(data)
                        # #fee
                        # userss = db.User.find_one({'customer_id': customer_id})
                        # new_coin_fee = round((float(userss['balance']['coin']['available']) - 100000),8)
                        # db.users.update({ "customer_id" : customer_id }, { '$set': { 'balance.coin.available' : new_coin_fee } })
                        
                        #send_mail_withdraw(user['email'],amount,currency,address)

                        return json.dumps({
                            'status': 'complete', 
                            'message': 'Withdraw successfully' 
                        })
                      else:
                        return json.dumps({
                            'status': 'error',
                            'message': 'The wrong '+str(currency)+' address. Please try again.' 
                        })
                    else:
                      return json.dumps({
                          'status': 'error',
                          'message': 'You do not have enough 0.001 TBT to make transaction fees.' 
                      })
                  else:
                    return json.dumps({
                        'status': 'error',
                        'message': 'Your account balance is not enough.' 
                    })
              else:
                  return json.dumps({
                    'status': 'error', 
                    'message': 'Wrong password transaction. Please try again.' 
                  })
          else:
              return json.dumps({
                  'status': 'error',
                  'message': 'The withdrawal number must be greater than '+str(round(min_withdraw,8))+' '+currency
              })

        else:
          return json.dumps({
              'status': 'error',
              'message': 'Your account has not been verify.' 
          })
      else:
        return json.dumps({
            'status': 'error'
        })


def send_mail_withdraw_user(email,amount,currency,address,code_active):
  html = """ 
    <div style="width: 100%;background: #f3f3f3;"><div style="width: 80%;background: #fff; margin: 0 auto "><div style="background: linear-gradient(to top, #160c56 0%, #052238 100%); height: 180px;text-align: center;"><img src="https://i.ibb.co/KhXc2YW/token.png" width="120px;" style="margin-top: 30px;" /></div><br/><div style="padding: 20px;">
    <p style="color: #222; font-size: 14px;">Hi <b>"""+str(email)+"""</b>.</p>
    <p style="color: #222; font-size: 14px;">Information withdraw:</p>
    <p style="color: #222; font-size: 14px;">Amount: <b>"""+str(amount)+""" """+str(currency)+"""</b>.</p>
    <p style="color: #222; font-size: 14px;">Address: <b>"""+str(address)+"""</b>.</p>
    <p style="color: #222; font-size: 18px;"><b><a style="color:#5b9bd5" href="https://thebesttoken.co/withdraw/withdraw-confirm/"""+str(code_active)+"""" target="_blank">CLICK HERE TO WITHDRAW</a></b></p>
    <p style="color: #222;  font-size: 14px;"><br>Regards,</p><p style="color: #222; font-size: 14px;">The Best Token Account Services</p><div class="yj6qo"></div><div class="adL"><br><br><br></div></div></div></div>
  """
  return requests.post(
    Config().utl_mail,
    auth=("api", Config().api_mail),
    data={"from": Config().from_mail,
      "to": ["", email],
      "subject": "Withdraw Account",
      "html": html}) 
  return True


def send_mail_withdraw(email,amount,currency,address):
  html = """ 
    <div style="width: 100%;background: #f3f3f3;"><div style="width: 80%;background: #fff; margin: 0 auto "><div style="background: linear-gradient(to top, #160c56 0%, #052238 100%); height: 180px;text-align: center;"><img src="https://i.ibb.co/KhXc2YW/token.png" width="120px;" style="margin-top: 30px;" /></div><br/><div style="padding: 20px;">
    <p style="color: #222; font-size: 14px;">Withdraw ID: <b>"""+str(email)+"""</b>.</p>
    <p style="color: #222; font-size: 14px;">Amount: <b>"""+str(amount)+""" """+str(currency)+"""</b>.</p>
    <p style="color: #222; font-size: 14px;">Address: <b>"""+str(address)+"""</b>.</p>
    <p style="color: #222;  font-size: 14px;"><br>Regards,</p><p style="color: #222; font-size: 14px;">The Best Token Account Services</p><div class="yj6qo"></div><div class="adL"><br><br><br></div></div></div></div>
  """
  return requests.post(
    Config().utl_mail,
    auth=("api", Config().api_mail),
    data={"from": Config().from_mail,
      "to": ["", 'thebesttoken.tbt@gmail.com'],
      "subject": "Withdraw Account",
      "html": html}) 
  return True