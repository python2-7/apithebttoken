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
import time
import requests
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
sys.setrecursionlimit(10000)
digits58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

from rex.coinpayments import CoinPaymentsAPI
from rex.config import Config

ApiCoinpayment = CoinPaymentsAPI(public_key=Config().public_key,
                          private_key=Config().private_key)

__author__ = 'asdasd'

apiinvestment_ctrl = Blueprint('investment', __name__, static_folder='static', template_folder='templates')
def check_password(pw_hash, password):
        return check_password_hash(pw_hash, password)
@apiinvestment_ctrl.route('/dailyprofit-alsjaldjaslkdladadjaaskjd', methods=['GET', 'POST'])
def testinvest():
    
    caculator_profitDaily()

    return json.dumps({
        'status': 'dailyprofit-complete' 
        
    })

@apiinvestment_ctrl.route('/active-package', methods=['GET', 'POST'])
def active_package():
    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id']
    currency = dataDict['currency']
    amount = dataDict['amount']
    password_transaction = dataDict['password_transaction']

    user = db.User.find_one({'customer_id': customer_id})

    if check_password(user['password_transaction'], password_transaction) == True or 1==1:

        if user is not None:
            ticker = db.tickers.find_one({})
            if currency == 'BTC': 
                price_atlcoin = ticker['btc_usd']
                string_query = 'balance.bitcoin.available'
                val_balance = user['balance']['bitcoin']['available']
            if currency == 'ETH':
                price_atlcoin = ticker['eth_usd']
                string_query = 'balance.ethereum.available'
                val_balance = user['balance']['ethereum']['available']
            if currency == 'LTC':
                price_atlcoin = ticker['ltc_usd']
                string_query = 'balance.litecoin.available'
                val_balance = user['balance']['litecoin']['available']
            if currency == 'XRP':
                price_atlcoin = ticker['xrp_usd']
                string_query = 'balance.ripple.available'
                val_balance = user['balance']['ripple']['available']
            if currency == 'USDT':
                price_atlcoin = ticker['usdt_usd']
                string_query = 'balance.tether.available'
                val_balance = user['balance']['tether']['available']
            if currency == 'DASH':
                price_atlcoin = ticker['dash_usd']
                string_query = 'balance.dash.available'
                val_balance = user['balance']['dash']['available']
            if currency == 'EOS':
                price_atlcoin = ticker['eso_usd']
                string_query = 'balance.eos.available'
                val_balance = user['balance']['eos']['available']
            if currency == 'BCH':
                price_atlcoin = ticker['bch_usd']
                string_query = 'balance.bitcoincash.available'
                val_balance = user['balance']['bitcoincash']['available']
            if currency == 'DOGE':
                price_atlcoin = ticker['doge_usd']
                string_query = 'balance.dogecoin.available'
                val_balance = user['balance']['dogecoin']['available']
            if currency == 'TBT':
                price_atlcoin = ticker['coin_usd']
                string_query = 'balance.coin.available'
                val_balance = user['balance']['coin']['available']

            if float(val_balance) >= float(amount)*100000000:
                amount_usd = round(float(amount)*float(price_atlcoin),2)
                if float(amount_usd) >= 100:

                    if float(amount_usd) >= 100 and float(amount_usd) < 1000:
                        percent_daily = 0.3
                    if float(amount_usd) >= 1000 and float(amount_usd) < 5000:
                        percent_daily = 0.5
                    if float(amount_usd) >= 5000 and float(amount_usd) < 15000:
                        percent_daily = 0.6
                    if float(amount_usd) >= 15000 and float(amount_usd) < 25000:
                        percent_daily = 0.8
                    if float(amount_usd) >= 25000:
                        percent_daily = 1

                    new_balance_sub = round((float(val_balance) - float(amount)*100000000),8)

                    new_invest_ss = float(user['investment'])+float(amount_usd)

                    db.users.update({ "customer_id" : customer_id }, { '$set': { string_query: float(new_balance_sub),'investment' : new_invest_ss} })
                    
                    #save lich su
                    data_investment = {
                        'uid' : customer_id,
                        'user_id': str(user['_id']),
                        'username' : user['email'],
                        'amount_usd' : float(amount_usd),
                        'package': round(float(amount),8),
                        'status' : 1,
                        'date_added' : datetime.utcnow(),
                        'amount_frofit' : 0,
                        'coin_amount' : 0,
                        'total_income' : '',
                        'status_income' : 0,
                        'date_income' : '',
                        'date_profit' : datetime.utcnow(), #+ timedelta(days=3)
                        'currency' : currency,
                        'percent_daily' : percent_daily
                    }
                    db.investments.insert(data_investment)

                    #save dialing
                    # data_dialing = {
                    #     'customer_id' : customer_id,
                    #     'username' : user['email'],
                    #     'package': round(float(amount),8),
                    #     'status' : 0,
                    #     'date_added' : datetime.utcnow(),
                    #     'amount_coin' : 0,
                    #     'currency' : currency
                    # }
                    # db.dialings.insert(data_dialing)


                    #FnRefferalProgram(customer_id, amount, currency)

                    TotalnodeAmount(customer_id, amount_usd)

                    return json.dumps({
                        'status': 'complete', 
                        'message': 'Ai-dog successfully' 
                    })
                else:
                    return json.dumps({
                        'status': 'error',
                        'message': 'The minimum amount of ai-dog is '+str(round(100/float(price_atlcoin),8))+' '+currency 
                    })
            else:
                return json.dumps({
                    'status': 'error',
                    'message': 'Account balance is not enough to Ai-dog' 
                })

        else:
          return json.dumps({
              'status': 'error'
          })
    else:
        return json.dumps({
            'status': 'error', 
            'message': 'Wrong password transaction. Please try again' 
        })
    


@apiinvestment_ctrl.route('/disable-package', methods=['GET', 'POST'])
def disable_package():

    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id']
    currency = dataDict['currency']
    
    val_add_balance = 0
    amount_usd_sub = 0
    now_date= datetime.utcnow()

    investment = db.investments.find({'$and' : [{'uid': customer_id},{'currency': currency},{'status' : 1}]})
    for item in investment:

        sub_date = now_date - item['date_added']
        if int(sub_date.days) < 20:
            percent_fee = 5
        if int(sub_date.days) >= 21:
            percent_fee = 1
        
        percent_fee = 100 - float(percent_fee)
        val_add_balance += float(item['package'])*float(percent_fee)*1000000
        amount_usd_sub += float(item['amount_usd'])
        db.investments.update({ "_id" : ObjectId(item['_id']) }, { '$set': { 'status': 0} })

    user = db.User.find_one({'customer_id': customer_id})

    if currency == 'BTC': 
        string_query = 'balance.bitcoin.available'
        val_balance = user['balance']['bitcoin']['available']
    if currency == 'ETH':
        string_query = 'balance.ethereum.available'
        val_balance = user['balance']['ethereum']['available']
    if currency == 'LTC':
        string_query = 'balance.litecoin.available'
        val_balance = user['balance']['litecoin']['available']
    if currency == 'XRP':
        string_query = 'balance.ripple.available'
        val_balance = user['balance']['ripple']['available']
    if currency == 'USDT':
        string_query = 'balance.tether.available'
        val_balance = user['balance']['tether']['available']
    if currency == 'DASH':
        string_query = 'balance.dash.available'
        val_balance = user['balance']['dash']['available']
    if currency == 'EOS':
        string_query = 'balance.eos.available'
        val_balance = user['balance']['eos']['available']
    if currency == 'BCH':
        string_query = 'balance.bitcoincash.available'
        val_balance = user['balance']['bitcoincash']['available']
    if currency == 'DOGE':
        string_query = 'balance.dogecoin.available'
        val_balance = user['balance']['dogecoin']['available']
    if currency == 'TBT':
        string_query = 'balance.coin.available'
        val_balance = user['balance']['coin']['available']

    new_balance_add = float(val_balance) + float(val_add_balance)

              
    db.users.update({ "customer_id" : customer_id }, { '$set': { string_query: float(new_balance_add)} })

    TotalnodeAmountSub(customer_id,amount_usd_sub)

    customer = db.User.find_one({'customer_id': customer_id})

    investments = db.investments.find({'$and' : [{'uid': customer_id},{'status' : 1}]})
    investment_usd = 0
    for items in investments:
        investment_usd += float(items['amount_usd'])
    if  float(investment_usd) > 0:
        db.users.update({ "customer_id" : customer_id }, { '$set': { 'investment' : investment_usd } })

    
    return json.dumps({
        'status': 'complete', 
        'message': 'Disable Ai-Dog successfully' 
    })
@apiinvestment_ctrl.route('/get-history', methods=['GET', 'POST'])
def get_historys_investment():

    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id']
    start = dataDict['start']
    limit = dataDict['limit']
    investment = db.investments.find({'uid': customer_id}).sort([("date_added", -1)]).limit(limit).skip(start)

    
    array = []
    for item in investment:
      array.append({
        "username" : item['username'],
        "package" : item['package'],
        "currency" : item['currency'],
        "status" : item['status'],
        "amount_usd" : item['amount_usd'],
        "date_added" : (item['date_added']).strftime('%H:%M %d-%m-%Y')
      })
    return json.dumps(array)

@apiinvestment_ctrl.route('/get-active-invest', methods=['GET', 'POST'])
def get_active_investment():

    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id']
   
    investment = db.investments.find({'$and' :[{'uid': customer_id},{'status' : 1}]})

    
    array = []
    for item in investment:
      array.append({
        "package" : item['package'],
        "currency" : item['currency'],
        "amount_usd" : item['amount_usd'],
        "date_added" : (item['date_added']).strftime('%H:%M %d-%m-%Y')
      })
    return json.dumps(array)

@apiinvestment_ctrl.route('/get-active-invest-currency', methods=['GET', 'POST'])
def get_active_investment_currency():

    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id']
    currency = dataDict['currency']
    investment = db.investments.find({'$and' :[{'uid': customer_id},{'status' : 1},{'currency' : currency}]})

    
    amount_invest = 0
    for item in investment:
        amount_invest += float(item['package'])
    return json.dumps({
        'status': 'complete', 
        'amount': amount_invest 
    })

@apiinvestment_ctrl.route('/submit-payment', methods=['GET', 'POST'])
def submit_payment():
    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id']
    address = dataDict['address']
    currency = dataDict['currency']
    amount = dataDict['amount']
    password_transaction = dataDict['password_transaction']

    user = db.User.find_one({'customer_id': customer_id})
    if int(user['security']['email']['status']) == 1:
        if check_password(user['password_transaction'], password_transaction) == True:

            if user is not None:
                ticker = db.tickers.find_one({})
                if currency == 'BTC': 
                    price_atlcoin = ticker['btc_usd']
                    string_query = 'balance.bitcoin.available'
                    string_query_address = 'balance.bitcoin.cryptoaddress'
                    val_balance = user['balance']['bitcoin']['available']
                if currency == 'ETH':
                    price_atlcoin = ticker['eth_usd']
                    string_query = 'balance.ethereum.available'
                    val_balance = user['balance']['ethereum']['available']
                    string_query_address = 'balance.ethereum.cryptoaddress'
                if currency == 'LTC':
                    price_atlcoin = ticker['ltc_usd']
                    string_query = 'balance.litecoin.available'
                    val_balance = user['balance']['litecoin']['available']
                    string_query_address = 'balance.litecoin.cryptoaddress'
                if currency == 'XRP':
                    price_atlcoin = ticker['xrp_usd']
                    string_query = 'balance.ripple.available'
                    val_balance = user['balance']['ripple']['available']
                    string_query_address = 'balance.ripple.cryptoaddress'
                if currency == 'USDT':
                    price_atlcoin = ticker['usdt_usd']
                    string_query = 'balance.tether.available'
                    val_balance = user['balance']['tether']['available']
                    string_query_address = 'balance.tether.cryptoaddress'
                if currency == 'DASH':
                    price_atlcoin = ticker['dash_usd']
                    string_query = 'balance.dash.available'
                    val_balance = user['balance']['dash']['available']
                    string_query_address = 'balance.dash.cryptoaddress'
                if currency == 'EOS':
                    price_atlcoin = ticker['eso_usd']
                    string_query = 'balance.eos.available'
                    val_balance = user['balance']['eos']['available']
                    string_query_address = 'balance.eos.cryptoaddress'

                if currency == 'BCH':
                    price_atlcoin = ticker['bch_usd']
                    string_query = 'balance.bitcoincash.available'
                    val_balance = user['balance']['bitcoincash']['available']
                    string_query_address = 'balance.bitcoincash.cryptoaddress'
                if currency == 'DOGE':
                    price_atlcoin = ticker['doge_usd']
                    string_query = 'balance.dogecoin.available'
                    val_balance = user['balance']['dogecoin']['available']
                    string_query_address = 'balance.dogecoin.cryptoaddress'
                if currency == 'TBT':
                    price_atlcoin = ticker['coin_usd']
                    string_query = 'balance.coin.available'
                    val_balance = user['balance']['coin']['available']
                    string_query_address = 'balance.coin.cryptoaddress'

                if float(val_balance) >= float(amount)*100000000:
                        amount_usd = float(amount)*float(price_atlcoin)

                        user_receve = db.User.find_one({string_query_address: address})
                        
                        if user_receve is not None:


                            new_balance_sub = round((float(val_balance) - float(amount)*100000000),8)
                          
                            db.users.update({ "customer_id" : customer_id }, { '$set': { string_query: float(new_balance_sub)} })
                            
                            if currency == 'BTC': 
                                price_atlcoin = ticker['btc_usd']
                                string_query = 'balance.bitcoin.available'
                                val_balance_receve = user_receve['balance']['bitcoin']['available']
                            if currency == 'ETH':
                                price_atlcoin = ticker['eth_usd']
                                string_query = 'balance.ethereum.available'
                                val_balance_receve = user_receve['balance']['ethereum']['available']
                            if currency == 'LTC':
                                price_atlcoin = ticker['ltc_usd']
                                string_query = 'balance.litecoin.available'
                                val_balance_receve = user_receve['balance']['litecoin']['available']
                            if currency == 'XRP':
                                price_atlcoin = ticker['xrp_usd']
                                string_query = 'balance.ripple.available'
                                val_balance_receve = user_receve['balance']['ripple']['available']
                            if currency == 'USDT':
                                price_atlcoin = ticker['usdt_usd']
                                string_query = 'balance.tether.available'
                                val_balance_receve = user_receve['balance']['tether']['available']
                            if currency == 'DASH':
                                price_atlcoin = ticker['dash_usd']
                                string_query = 'balance.dash.available'
                                val_balance_receve = user_receve['balance']['dash']['available']
                            if currency == 'EOS':
                                price_atlcoin = ticker['eso_usd']
                                string_query = 'balance.eos.available'
                                val_balance_receve = user_receve['balance']['eos']['available']
                            
                            if currency == 'BCH':
                                price_atlcoin = ticker['bch_usd']
                                string_query = 'balance.bitcoincash.available'
                                val_balance_receve = user_receve['balance']['bitcoincash']['available']
                                
                            if currency == 'DOGE':
                                price_atlcoin = ticker['doge_usd']
                                string_query = 'balance.dogecoin.available'
                                val_balance_receve = user_receve['balance']['dogecoin']['available']
                                

                            if currency == 'TBT':
                                price_atlcoin = ticker['coin_usd']
                                string_query = 'balance.coin.available'
                                val_balance_receve = user_receve['balance']['coin']['available']

                            new_balance_add = round((float(val_balance_receve) + float(amount)*100000000),8)
                          
                            db.users.update({ "customer_id" : user_receve['customer_id'] }, { '$set': { string_query: float(new_balance_add)} })
                            
                            #save lich su
                            data_payment_sub = {
                                'uid' : customer_id,
                                'user_id': str(user['_id']),
                                'username' : user['email'],
                                'amount_usd' : float(amount_usd),
                                'amount' : amount,
                                'status' : 1,
                                'date_added' : datetime.utcnow(),
                                'address' : address,
                                'currency' : currency,
                                'types' : 'send'
                            }
                            db.payments.insert(data_payment_sub)

                            data_payment_add = {
                                'uid' : user_receve['customer_id'],
                                'user_id': str(user_receve['_id']),
                                'username' : user_receve['email'],
                                'amount_usd' : float(amount_usd),
                                'amount' : amount,
                                'status' : 1,
                                'date_added' : datetime.utcnow(),
                                'address' : address,
                                'currency' : currency,
                                'types' : 'receive'
                            }
                            db.payments.insert(data_payment_add)

                            
                            return json.dumps({
                                'status': 'complete', 
                                'message': 'Payment successfully' 
                            })
                        else:
                            return json.dumps({
                                'status': 'error',
                                'message': 'Awrong payment information' 
                            })
                   
                else:
                    return json.dumps({
                        'status': 'error',
                        'message': 'Account balance is not enough to payment' 
                    })

            else:
              return json.dumps({
                  'status': 'error'
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

@apiinvestment_ctrl.route('/get-history-payment', methods=['GET', 'POST'])
def get_history_payment():

    dataDict = json.loads(request.data)
    customer_id = dataDict['customer_id']
    start = dataDict['start']
    limit = dataDict['limit']
    investment = db.payments.find({'uid': customer_id}).sort([("date_added", -1)]).limit(limit).skip(start)

    
    array = []
    for item in investment:
      array.append({

        "username" : item['username'],
        "amount" : item['amount'],
        "currency" : item['currency'],
        "status" : item['status'],
        "address" : item['address'],
        "types" : item['types'],
        "date_added" : (item['date_added']).strftime('%H:%M %d-%m-%Y')
      })
    return json.dumps(array)

def FnRefferalProgram(customer_id, amount_invest, currency):
    customers = db.users.find_one({"customer_id" : customer_id })
    if customers['p_node'] != '':
        customers_pnode = db.users.find_one({"customer_id" : customers['p_node'] })

        if float(customers_pnode['investment'] > 0):
            ticker = db.tickers.find_one({})

            if currency == 'BTC': 
                price_atlcoin = ticker['btc_usd']
                string_query = 'balance.bitcoin.available'
                val_balance = customers_pnode['balance']['bitcoin']['available']
            if currency == 'ETH':
                price_atlcoin = ticker['eth_usd']
                string_query = 'balance.ethereum.available'
                val_balance = customers_pnode['balance']['ethereum']['available']
            if currency == 'LTC':
                price_atlcoin = ticker['ltc_usd']
                string_query = 'balance.litecoin.available'
                val_balance = customers_pnode['balance']['litecoin']['available']
            if currency == 'XRP':
                price_atlcoin = ticker['xrp_usd']
                string_query = 'balance.ripple.available'
                val_balance = customers_pnode['balance']['ripple']['available']
            if currency == 'USDT':
                price_atlcoin = ticker['usdt_usd']
                string_query = 'balance.tether.available'
                val_balance = customers_pnode['balance']['tether']['available']
            if currency == 'DASH':
                price_atlcoin = ticker['dash_usd']
                string_query = 'balance.dash.available'
                val_balance = customers_pnode['balance']['dash']['available']
            if currency == 'EOS':
                price_atlcoin = ticker['eso_usd']
                string_query = 'balance.eos.available'
                val_balance = customers_pnode['balance']['eos']['available']
            if currency == 'TBT':
                price_atlcoin = ticker['coin_usd']
                string_query = 'balance.coin.available'
                val_balance = customers_pnode['balance']['coin']['available']

           
            
            commission = float(price_atlcoin)*float(amount_invest)*0.03

            r_wallet = float(customers_pnode['r_wallet'])
            new_r_wallet = float(r_wallet) + float(commission)
            new_r_wallet = float(new_r_wallet)

            total_earn = float(customers_pnode['total_earn'])
            new_total_earn = float(total_earn) + float(commission)
            new_total_earn = float(new_total_earn)

            balance_wallet = float(val_balance)
            new_balance_wallet = float(balance_wallet) + (float(amount_invest)*0.03*100000000)
            new_balance_wallet = round(float(new_balance_wallet),8)

            db.users.update({ "_id" : ObjectId(customers_pnode['_id']) }, { '$set': {string_query : new_balance_wallet,'total_earn': new_total_earn, 'r_wallet' :new_r_wallet } })
            
            detail = str(customers['email']) + ' Ai-dog '+ str(amount_invest) + ' ' + str(currency)
            SaveHistory(customers_pnode['customer_id'],customers_pnode['email'],detail, float(amount_invest)*0.03, currency, 'Direct commission')
   
    return True

def caculator_profitDaily():
    get_invest = db.investments.find({ "status": 1});
    ticker = db.tickers.find_one({})
    price_coin = ticker['coin_usd']
    
    percent = 0.3
    for x in get_invest:
        
        customer = db.users.find_one({'customer_id': x['uid']})
        if customer is not None:

            commission = float(x['amount_usd'])*float(percent)/100

            d_wallet = float(customer['d_wallet'])
            new_d_wallet = float(d_wallet) + float(commission)
            new_d_wallet = float(new_d_wallet)

            total_earn = float(customer['total_earn'])
            new_total_earn = float(total_earn) + float(commission)
            new_total_earn = float(new_total_earn)


            new_balance_wallet = float(commission)/float(ticker['coin_usd'])
            new_balance_wallet = round((float(customer['balance']['coin']['available']) + (float(new_balance_wallet)*100000000)),8)

            db.users.update({ "_id" : ObjectId(customer['_id']) }, { '$set': {'balance.coin.available' : new_balance_wallet,'total_earn': new_total_earn, 'd_wallet' :new_d_wallet } })
            

            db.investments.update({ "_id" : ObjectId(x['_id']) }, { '$set': {'amount_frofit' : float(x['amount_frofit'])+(float(commission)/float(ticker['coin_usd'])) } })
            detail = str(percent) + '% - Ai-dog '+ str(x['package']) + ' ' + str( x['currency'])
            SaveHistory(customer['customer_id'],customer['email'],detail, round(float(commission)/float(ticker['coin_usd']),8), 'TBT', 'Profit day')
            
            #print customer['customer_id'],round((float(commission)/float(ticker['coin_usd'])),8),'TOKEN'

            Systemcommission(customer['customer_id'],round((float(commission)/float(ticker['coin_usd'])),8),'TBT')


    return True

def Systemcommission(customer_id,amount_receive,currency):
    customers = db.users.find_one({"customer_id" : customer_id })
    email_customer_receive = customers['email']
    ticker = db.tickers.find_one({})
    i = 0
    while i < 9:
        i += 1 
        if customers['p_node'] != '':
            customers = db.users.find_one({"customer_id" : customers['p_node'] })
            if customers is None:
                return True
            else:
                percent_receve = 0

                count_f1 = db.users.find({'$and' : [{"p_node" : customers['customer_id'] },{ 'investment': { '$gt': 0 } }]} ).count()

                if int(count_f1) >=1 and i == 1:
                    #hoa hong dong 1 - 100%
                    percent_receve = 100

                if int(count_f1) >=2 and i == 2:
                    #hoa hong dong 2 - 10%
                    percent_receve = 20
                if int(count_f1) >=2 and i == 3:
                    #hoa hong dong 3 - 10%
                    percent_receve = 20

                if int(count_f1) >=3 and i == 4:
                    #hoa hong dong 4 - 10%
                    percent_receve = 15
                if int(count_f1) >=3 and i == 5:
                    #hoa hong dong 5 - 10%
                    percent_receve = 15
                if int(count_f1) >=4 and i == 6:
                    #hoa hong dong 6 - 10%
                    percent_receve = 10
                if int(count_f1) >=4 and i == 7:
                    #hoa hong dong 7 - 10%
                    percent_receve = 10
                if int(count_f1) >=4 and i == 8:
                    #hoa hong dong 8 - 10%
                    percent_receve = 10
                
                if int(percent_receve) > 0:
                    
                    commission_coin = float(amount_receive)*float(percent_receve)*1000000

                    commission_usd = float(amount_receive)*float(percent_receve)*float(ticker['coin_usd'])/100

                    s_wallet = float(customers['s_wallet'])
                    new_s_wallet = float(s_wallet) + float(commission_usd)
                    new_s_wallet = float(new_s_wallet)

                    total_earn = float(customers['total_earn'])
                    new_total_earn = float(total_earn) + float(commission_usd)
                    new_total_earn = float(new_total_earn)

                    new_balance_wallet = round(float(customers['balance']['coin']['available']) + float(commission_coin),8)

                    db.users.update({ "_id" : ObjectId(customers['_id']) }, { '$set': {'balance.coin.available' : new_balance_wallet,'total_earn': new_total_earn, 's_wallet' :new_s_wallet } })
                    
                    detail = 'F'+str(i)+' '+ str(email_customer_receive) + ' received ' + str(amount_receive)+ ' ' +str( currency)
                    SaveHistory(customers['customer_id'],customers['email'],detail, round(float(commission_coin)/100000000,8), currency, 'System commission')
        else:
            break
    return True




def SaveHistory(uid, username,detail, amount, currency,types):
    data_history = {
        'uid':  uid,
        'username': username,
        'detail':  detail,
        'amount': round(amount,8),
        'currency' :  currency,
        'type' : types,
        'date_added' : datetime.utcnow()
    }
    db.historys.insert(data_history)
    return True

def TotalnodeAmount(user_id, amount_invest_usd):
    ticker = db.tickers.find_one({})
    customer_ml = db.users.find_one({"customer_id" : user_id })

    if customer_ml['p_node'] != '':
        while (True):
            customer_ml_p_node = db.users.find_one({"customer_id" : customer_ml['p_node'] })
            if customer_ml_p_node is None:
                break
            else:
                customers = db.users.find_one({"customer_id" : customer_ml_p_node['customer_id'] })
                customers['total_node'] = float(customers['total_node']) + float(amount_invest_usd)
                db.users.save(customers)
                
            customer_ml = db.users.find_one({"customer_id" : customer_ml_p_node['customer_id'] })
            if customer_ml is None:
                break
    return True

def TotalnodeAmountSub(user_id, amount_invest_usd):
    ticker = db.tickers.find_one({})
    customer_ml = db.users.find_one({"customer_id" : user_id })

    if customer_ml['p_node'] != '':
        while (True):
            customer_ml_p_node = db.users.find_one({"customer_id" : customer_ml['p_node'] })
            if customer_ml_p_node is None:
                break
            else:
                customers = db.users.find_one({"customer_id" : customer_ml_p_node['customer_id'] })
                customers['total_node'] = float(customers['total_node']) - float(amount_invest_usd)
                db.users.save(customers)
                
            customer_ml = db.users.find_one({"customer_id" : customer_ml_p_node['customer_id'] })
            if customer_ml is None:
                break
    return True