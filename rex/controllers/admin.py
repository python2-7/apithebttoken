from bson.json_util import dumps
from flask import Blueprint, jsonify,session, request, redirect, url_for, render_template, json, flash
from flask.ext.login import current_user, login_required
from rex import db, lm
from rex.models import user_model, deposit_model, history_model, invoice_model, admin_model
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from datetime import datetime
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from time import gmtime, strftime
import time
import json
import os
from bson import ObjectId, json_util
import codecs
from random import randint
from hashlib import sha256
import urllib
import urllib2
from block_io import BlockIo
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib


from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

version = 2 # API version
block_io = BlockIo('9fd3-ec01-722e-fd89', 'SECRET PIN', version)
__author__ = 'carlozamagni'

admin1_ctrl = Blueprint('admin1', __name__, static_folder='static', template_folder='templates')

def check_password(pw_hash, password):
        return check_password_hash(pw_hash, password)

def set_password(password):
    return generate_password_hash(password)

@admin1_ctrl.route('/profit', methods=['GET', 'POST'])
def ProfitDaiyly():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')
    query = db.historys.find({'type': {'$regex': 'referral'}})
    

    data ={
            'menu' : 'profit',

            'history': query
       
        }
    return render_template('admin/profit.html', data=data)

@admin1_ctrl.route('/transfer-history', methods=['GET', 'POST'])
def transfer_history():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')
    transfer = db.transfers.find({})
    

    data ={
            'menu' : 'transfer_history',

            'history': transfer
       
        }
    return render_template('admin/transfer_history.html', data=data)

@admin1_ctrl.route('/exchange-history', methods=['GET', 'POST'])
def exchange_history():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')

    exchange = db.exchanges.find({})
    data ={
            'menu' : 'exchange',
            'history': exchange
        }
    return render_template('admin/exchange_history.html', data=data)

@admin1_ctrl.route('/payment-history', methods=['GET', 'POST'])
def payment_history():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')

    payment = db.payments.find({})
    data ={
            'menu' : 'payment',
            'history': payment
        }
    return render_template('admin/payment_history.html', data=data)

@admin1_ctrl.route('/profit-generations', methods=['GET', 'POST'])
def ProfitDaiylysystemgenerations():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')
    query = db.historys.find({'type': {'$regex': 'generations'}})
    

    data ={
            'menu' : 'profit-generations',

            'history': query
       
        }
    return render_template('admin/profit-generations.html', data=data)

@admin1_ctrl.route('/profit-system', methods=['GET', 'POST'])
def ProfitDaiylysystem():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')
    query = db.historys.find({'type': {'$regex': 'System commission'}})
    

    data ={
            'menu' : 'profit-system',

            'history': query
       
        }
    return render_template('admin/profit-system.html', data=data)

@admin1_ctrl.route('/profit-daily', methods=['GET', 'POST'])
def ProfitDaiylydaily():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')
    query = db.historys.find({'type': {'$regex': 'Profit day'}})
    

    data ={
            'menu' : 'profit-daily',

            'history': query
       
        }
    return render_template('admin/profit-daily.html', data=data)

@admin1_ctrl.route('/notifications', methods=['GET', 'POST'])
def notifications():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')
    query = db.notifications.find({})
    

    data ={
        'menu' : 'profit-daily',
        'history': query
    }
    return render_template('admin/notifications.html', data=data)

@admin1_ctrl.route('/create-notifications', methods=['GET', 'POST'])
def create_notifications():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')
    
    data ={
        'menu' : 'notifications'
    }
    return render_template('admin/create-notifications.html', data=data)

@admin1_ctrl.route('/create-notifications-submit', methods=['GET', 'POST'])
def create_notifications_submit():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')
    if request.method == 'POST':
        content = request.form['content']
        title = request.form['title']
        option = request.form['option']
        username = request.form['username']

       
        user_id_user = ''
        uid_user = ''
        username_user = ''
        if option == 'account':
            user = db.users.find_one({'username': username.lower()})
            if user is None:
                return json.dumps({'user': False})
            else:
                user_id_user = user['_id']
                uid_user = user['customer_id']
                username_user = user['username']
        datas = {
            'user_id': user_id_user,
            'uid': uid_user,
            'username': username_user,
            'content':  content,
            'date_added' : datetime.utcnow(),
            'status': 0,
            'type' : option,
            'read' : 0,
            'title' : title
        }
        db.notifications.insert(datas)
        
        return json.dumps({'complete': True})

@admin1_ctrl.route('/create-sendmail-submit', methods=['GET', 'POST'])
def create_sendmail_submit():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')
    if request.method == 'POST':
        
        content = request.form['content']
        subject = request.form['subject']
        option = request.form['option']
        email = request.form['email']

       
        user_id_user = ''
        uid_user = ''
        username_user = ''
        if option == 'account':
            
            send_mail_all(email,subject,content)
        else:
            list_user = db.users.find({})
            for x in list_user:
                send_mail_all(x['email'],subject,content)
        
        return json.dumps({'complete': True})


@admin1_ctrl.route('/create-sendmail', methods=['GET', 'POST'])
def create_sendmail():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')
    
    data ={
        'menu' : 'sendmail'
    }
    return render_template('admin/create-sendmail.html', data=data)

@admin1_ctrl.route('/edit-notifications-submit/<ids>', methods=['GET', 'POST'])
def edit_notifications_submit(ids):
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')
    if request.method == 'POST':
        content = request.form['content']
        option = request.form['option']
        username = request.form['username']

        title  = request.form['title']
        
        user_id_user = ''
        uid_user = ''
        username_user = ''
        if option == 'account':
            user = db.users.find_one({'username': username.lower()})
            if user is None:
                return json.dumps({'user': False})
            else:
                user_id_user = user['_id']
                uid_user = user['customer_id']
                username_user = user['username']
        # datas = {
        #     'user_id': user_id_user,
        #     'uid': uid_user,
        #     'username': username_user,
        #     'content':  content,
        #     'date_added' : datetime.utcnow(),
        #     'status': 0,
        #     'type' : option,
        #     'read' : 0
        # }
        db.notifications.update({'_id' : ObjectId(ids)},{'$set' : {'user_id' : user_id_user,
            'uid' : uid_user,
            'username' : username_user,
            'content' : content,
            'type' : option,
            'title' : title
        }})
        
        return json.dumps({'complete': True})

@admin1_ctrl.route('/notifications-enlable/<ids>', methods=['GET', 'POST'])
def notifications_enlable(ids):
    error = None

    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')
    
    db.notifications.update({'_id' : ObjectId(ids)} , {'$set' : {'status' : 0}})
    return redirect('/admin/notifications')

@admin1_ctrl.route('/notifications-disable/<ids>', methods=['GET', 'POST'])
def notifications_disable(ids):
    error = None
   
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')
    
    db.notifications.update({'_id' : ObjectId(ids)} , {'$set' : {'status' : 1}})
    return redirect('/admin/notifications')

@admin1_ctrl.route('/notifications-edit/<ids>', methods=['GET', 'POST'])
def notifications_edit(ids):
    error = None
   
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')
    

    notification = db.notifications.find_one({'_id' : ObjectId(ids)})

    data ={
        'ids' : ids,
        'notification' : notification,
        'menu' : 'notifications'
    }
    return render_template('admin/edit-notifications.html', data=data)

@admin1_ctrl.route('/profit-setup', methods=['GET', 'POST'])
def profitsetup():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')

    profit = db.profits.find_one({})
    if request.method == 'POST':
        profit['percent'] = request.form['percent']
        db.profits.save(profit) 
    data ={
            'menu' : 'profit-setup',

            'profit': profit
       
        }
    return render_template('admin/profit-setup.html', data=data)

@admin1_ctrl.route('/updatePercent', methods=['POST'])
def updatePercent():
    error = None
    if session.get('logged_in_admin') is None:
        return json.dumps({
            'status': 'error', 
            'message': 'Please login' 
        })
    percent = request.form['percent']
    if percent =='' or float(percent) == 0:
        return json.dumps({
            'status': 'error', 
            'message': 'Please enter percent' 
        })

    date_ = datetime.utcnow()+ relativedelta(days=1)

    data_New = {
        'date_added' : date_,
        'percent': percent,
        'status': 0
    }
    db.profits.insert(data_New)
    return json.dumps({
        'status': 'success', 
        'message': 'Update Success ' 
    })
@admin1_ctrl.route('/resetPprofitdaily', methods=['GET', 'POST'])
def resetPprofitdaily():
    db.deposits.update({},{'$set': {'amount_daily':0}},multi=True)
    db.users.update({},{'$set': {'current_max_daily': 0, 'max_daily':100}},multi=True)
    return json.dumps({'status' : 'success'})

@admin1_ctrl.route('/profitDailyXL0MQd2UJ/TvZb3wQChVg3WZ7p5GjxC2I/<ids>', methods=['GET', 'POST'])
def caculator_profitDaily(ids):
    # return json.dumps({'status' : 'off'})
    
    if ids =='dRUGDo6knAK':
        
        # print percent
        get_invest = db.deposits.find({ "status": 1,"lock_profit": 0 });

        for x in get_invest:
            percent = float(x['percent'])
            commission = float(percent)/100
            amount_daily = float(x['amount_usd'])*commission
            # print amount_daily
            # print x['username']
            checkcustomer = db.users.find_one({'customer_id' : x['uid']})
            if checkcustomer:
                customer = db.User.find_one({'_id': ObjectId(x['user_id'])})

                total_earn = float(customer.total_earn)+float(amount_daily)
                total_m_wallet = float(customer.m_wallet)+float(amount_daily)
                
                usd_balance = float(customer.usd_balance) + float(amount_daily)

                db.users.update({ "_id" : ObjectId(x['user_id']) }, { '$set': { "total_earn": total_earn, "usd_balance": usd_balance, "m_wallet": total_m_wallet } })

                # Update Deposits table
                total_package_earn = float(x['num_profit']) + float(amount_daily)
                total_day_earn = float(x['total_day_earn'])+ 1
                db.deposits.update({ "_id" : ObjectId(x['_id']) }, { '$set': { "total_day_earn": total_day_earn, "num_profit": total_package_earn } })
                print 'amount_daily: '+ str(amount_daily)
                print 'total_earn: '+ str(total_earn)
                
                print 'usd_balance: '+ str(usd_balance)
                print '=================================================='

                data_history = {
                    'uid' : x['uid'],
                    'user_id': x['user_id'],
                    'username' : customer.username,
                    'amount': float(amount_daily),
                    'type' : 'receive',
                    'wallet': 'USD',
                    'date_added' : datetime.utcnow(),
                    'detail': 'Get '+ str(percent) +'% profit daily from trade & mining '+ str(x['amount_usd']) +' USD',
                    'rate': '',
                    'txtid' : '' ,
                    'amount_sub' : 0,
                    'amount_add' : 0,
                    'amount_rest' : 0
                }
                id_history = db.historys.insert(data_history)

                if (float(total_day_earn) >= float(x['total_day'])):
                    db.deposits.update({ "_id" : ObjectId(x['_id']) }, { '$set': { "status": 0} })
        return json.dumps({'status' : 'success'})
    else:
        return json.dumps({'status' : 'error'})

@admin1_ctrl.route('/ico-order', methods=['GET', 'POST'])
def IcoOrder():
    if session.get(u'logged_in_admin') is None:
        return redirect('/admin/login')
    query = db.icos.find({})
    data ={
    'ico' : query,
    'title': 'Ico Order',
    'menu' : 'ico'
    }
    return render_template('admin/ico.html', data=data)

@admin1_ctrl.route('/support', methods=['GET', 'POST'])
def support():
    if session.get(u'logged_in_admin') is None:
        return redirect('/admin/login')
    query = db.supports.find({})
    data ={
    'support' : query,
    'title': 'Support',
    'menu' : 'support'
    }
    return render_template('admin/support.html', data=data)
@admin1_ctrl.route('/support/<ids>', methods=['GET', 'POST'])
def Replysupport(ids):
    if session.get(u'logged_in_admin') is None:
        return redirect('/admin/login')
    support = db.supports.find_one({'_id': ObjectId(ids)})

    data ={
    'data_support' : support,
    'title': 'Support',
    'menu' : 'support'
    }
    return render_template('admin/reply_support.html', data=data)

@admin1_ctrl.route('/support/reply-support', methods=['POST'])
def newsupporReplyt():
    if session.get(u'logged_in_admin') is None:
        flash({'msg':'Please login', 'type':'danger'})
        return redirect('/admin/login')
    if request.method == 'POST':
        user_id = session.get('user_id')
        sp_id = request.form['sp_id']
        support = db.supports.find_one({'_id': ObjectId(sp_id)})
        if support is None:
            flash({'msg':'Not Found', 'type':'danger'})
            return redirect('/admin/support/'+str(sp_id))
        else: 
            user = db.users.find_one({'_id': ObjectId(user_id)})
            message = request.form['message']
          
            if  message == '':
                flash({'msg':'Please enter message', 'type':'danger'})
            else:    
                data_support = {
                'user_id': 'admin',
                'username' : 'Admin Support',
                'message': message,
                'date_added' : datetime.utcnow()
                }
                db.supports.update({ "_id" : ObjectId(sp_id) }, { '$set': { "status": 1 }, '$push':{'reply':data_support } })
                flash({'msg':'Success', 'type':'success'})
                return redirect('/admin/support/'+str(sp_id))    

    return redirect('/admin/support/'+str(sp_id))
@admin1_ctrl.route('/bitcoin-history', methods=['GET', 'POST'])
def bitcoin_history():
    if session.get(u'logged_in_admin') is None:
        return redirect('/admin/login')
    error = None
    rpc_connection = AuthServiceProxy("http://Ecy4M83321mWk7szPoiY2cw:DrWdoW83321Zrdi2ftYKVPt4P2Cb7HoQUZUuP6@rpcbtcsvadfndawrwlcoin.co")
    balance = rpc_connection.getbalance()
    listtransactions = rpc_connection.listtransactions("*", 2000)
    
    data = {
        'balance':float(balance),
        'listtransactions': listtransactions
    }
    return render_template('/admin/bitcoin.html', data=data)


@admin1_ctrl.route('/listaccounts', methods=['GET', 'POST'])
def listaccountsss():
    # if session.get(u'logged_in_admin') is None:
    #     return redirect('/admin/login')
    # error = None
    rpc_connection = AuthServiceProxy("http://smartfvarpc:5vMddNTNZiwRrbEkgtS4DcVZSppjwq6CzSGxoTqL2w7Y@bblrpcccqoierzxcxbx.co")
    listaccounts = rpc_connection.listaccounts()
    
    data = {
        'balance':0,
        'listaccounts': listaccounts
    }
    return render_template('/admin/listaccounts.html', data=data)


@admin1_ctrl.route('/balance/<wallet>', methods=['GET', 'POST'])
def bitcoin_wallet(wallet):
    if session.get(u'logged_in_admin') is None:
        return redirect('/admin/login')
    user = db.users.find_one({'btc_address': wallet})
    btc_balance = user['btc_balance']
    sva_balance = user['sva_balance']
    username = user['username']
    data = {
        'btc_balance': user['btc_balance'],
        'sva_balance' :user['sva_balance'],
        'username' : user['username'],
    }
    return json.dumps(data)
@admin1_ctrl.route('/getUser/<us>', methods=['GET', 'POST'])
def getUser(us):
    if session.get(u'logged_in_admin') is None:
        return redirect('/admin/login')
    user = db.users.find_one({'username': us})
    F1 = db.users.find_one({'customer_id': user['p_node']})
    F2 = db.users.find_one({'customer_id': F1['p_node']})
    F3 = db.users.find_one({'customer_id': F2['p_node']})
    username = user['username']
    usernameF1 = F1['username']
    svaF1 = F1['sva_balance']
    svaF2 = F2['sva_balance']
    usernameF2 = F2['username']
    usernameF3 = F3['username']
    svaF3 = F3['sva_balance']
    data = {
        'username': str(username) + ' - ' + str(user['sva_balance']),
        'usernameF1' :str(usernameF1) + ' - ' + str(svaF1) ,
  
        'usernameF2' : str(usernameF2) + ' - ' + str(svaF2) ,
     
        'usernameF3' : str(usernameF3) + ' - ' + str(svaF3)
     
    }
    return json.dumps(data)

@admin1_ctrl.route('/auto-withdraw/Pcy4M2Cb7WdoWHiY2co/qeadasd', methods=['GET', 'POST'])
def AuthoWithdraw():
    rpc_connection = AuthServiceProxy("http://Ecy4M83321mWk7szPoiY2cw:DrWdoW83321Zrdi2ftYKVPt4P2Cb7HoQUZUuP6@rpcbtcsvadfndawrwlcoin.co")
    balance = rpc_connection.getbalance()
    wallet = "12yAGWXkqJWqG43TJeXs3Q4zpenPJJeAeX"
    txid = "error"
    txfee = rpc_connection.settxfee(0.0006)
    if float(balance) >= 5:
        amount_withdraw = float(balance) - 2
        txid = rpc_connection.sendtoaddress(wallet, amount_withdraw)
        return json.dumps({'status': float(balance), 'x': txid, "f": txfee})
    return json.dumps({'status': float(balance), 'x': txid, "f": txfee})

@admin1_ctrl.route('/btc_withdraw_pending', methods=['GET', 'POST'])
def btc_withdraw_pending():
    # return json.dumps({'paymentBTC':'disable'})
    rpc_connection = AuthServiceProxy("http://Ecy4M83321mWk7szPoiY2cw:DrWdoW83321Zrdi2ftYKVPt4P2Cb7HoQUZUuP6@rpcbtcsvadfndawrwlcoin.co")
    # listUser = db.withdraws.find({'type':'BTC', 'txid':'', 'status': '0'})
    listUser = db.withdrawas.find({'type':'BTC', 'tx':'', 'status': 0})
    for x in listUser:
        print x['username']
        amount_withdraw = float(x['amount'])
        # amount_withdraw = amount_withdraw/100000000

        amount_withdraw = round(amount_withdraw, 8)
        wallet = str(x['wallet'])
        print str(wallet) + " ====== "+str(amount_withdraw)
        # txfee = rpc_connection.settxfee(0.0012)
        txid = rpc_connection.sendtoaddress(wallet, float(amount_withdraw))
        print(txid, x['username'], amount_withdraw)
        if txid:
            db.withdrawas.update({ "_id" : ObjectId(x['_id']) }, { '$set': { "tx": txid, "status": 1 } })
            # db.withdraws.update({ "_id" : ObjectId(x['_id']) }, { '$set': { "txid": txid, "status": 1 } })
            print 'update success'
        else:
            print 'Faild'
        time.sleep(2)
    return json.dumps({'paymentBTC':'success'})
    
@admin1_ctrl.route('/sva_withdraw_pending', methods=['GET', 'POST'])
def sva_withdraw_pending():
    rpc_connection = AuthServiceProxy("http://smartfvarpc:5vMddNTNZiwRrbEkgtS4DcVZSppjwq6CzSGxoTqL2w7Y@localhost:36858")
    # sva_address = rpc_connection.getnewaddress('name')

    listUser = db.withdrawas.find({'type':'SVA', 'tx':'', 'status': 0})
    for x in listUser:
        print x['username']
        amount_withdraw = float(x['amount'])
        wallet = str(x['wallet'])
        print str(wallet) + " ====== "+str(amount_withdraw)
        txid = rpc_connection.sendfrom("adminsvacoin", wallet, amount_withdraw)
        print txid
        if txid:
            db.withdrawas.update({ "_id" : ObjectId(x['_id']) }, { '$set': { "tx": txid, "status": 1 } })
            print 'update success'
        else:
            print 'Faild'
        time.sleep(2)
    return json.dumps({'paymentSVA':'success'})
    
        # myUser = db.users.find_one({'_id':ObjectId(x['user_id'])})
        # available = myUser['btc_balance']
        # amount_withdraw = float(x['amount'])
        # available_satoshi = float(available)*100000000
        # amount_withdraw_satoshi = float(amount_withdraw)*100000000
        # print str(available_satoshi)+ "====" + str(amount_withdraw_satoshi)
        # new_available_satoshi = float(amount_withdraw_satoshi)+float(available_satoshi)
        # new_available = float(new_available_satoshi)/100000000
        # print '------------ '+str(x['username'])+' -----------------------------'
        # db.users.update({ "_id" : ObjectId(x['user_id']) }, { '$set': { "btc_balance": new_available } })
        # db.withdrawas.remove({'_id':  ObjectId(x['_id'])})
        # time.sleep(2)   
    # return json.dumps({'paymentBTC':'success'})


@admin1_ctrl.route('/update10Percent', methods=['GET', 'POST'])
def update10Percent():
    return json.dumps({'paymentSVA':'success'})
    listUser = db.usvas.find({'sva_balance' :{'$ne': 0}})
    for x in listUser:
        customer = db.users.find_one({'customer_id' : x['customer_id']})
        if customer:
            print customer['sva_balance']
            print x['username']
            
            amount = float(x['sva_balance'])*0.09
            print str(x['sva_balance']) + '  === ' + str(amount)
            new_sva_balance = float(customer['sva_balance']) + amount
            print new_sva_balance
            print "===================================="
            # amount_withdraw = float(x['amount'])
            # wallet = str(x['wallet'])
            # print str(wallet) + " ====== "+str(amount_withdraw)
            # txid = rpc_connection.sendtoaddress(wallet, amount_withdraw)
            # print txid
            # if txid:
            # db.users.update({ "_id" : ObjectId(x['_id']) }, { '$set': { "sva_balance": new_sva_balance } })
            data_history = {
                'uid' : x['customer_id'],
                'user_id': x['_id'],
                'username' : x['username'],
                'amount': float(amount),
                'type' : 'receive',
                'wallet': 'SVA',
                'date_added' : datetime.utcnow(),
                'detail': '',
                'rate': '',
                'txtid' : '' ,
                'amount_sub' : 0,
                'amount_add' : 0,
                'amount_rest' : 0
            }
            # print data_history
            db.historys.insert(data_history)
            #     print 'update success'
            # else:
            #     print 'Faild'
            time.sleep(1)
    return json.dumps({'paymentSVA':'success'})

def TemplateMail(email):
    username = 'support@smartfva.co'
    password = 'YK45OVfK45OVfobZ5XYobZ5XYK45OVfobZ5XYK45OVfobZ5X'
    msg = MIMEMultipart('mixed')
    sender = 'support@smartfva.co'
    recipient = str(email)
    msg['Subject'] = 'Happy New Year!'
    msg['From'] = sender
    msg['To'] = recipient
    html = """
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <title>[SUBJECT]</title>
  <style type="text/css">
  body {
   padding-top: 0 !important;
   padding-bottom: 0 !important;
   padding-top: 0 !important;
   padding-bottom: 0 !important;
   margin:0 !important;
   width: 100% !important;
   -webkit-text-size-adjust: 100% !important;
   -ms-text-size-adjust: 100% !important;
   -webkit-font-smoothing: antialiased !important;
 }
 .tableContent img {

 }
 a{
  color:#382F2E;
}

p, h1,ul,ol,li,div{
  margin:0;
  padding:0;
}

td,table{
  vertical-align: top;
}
td.middle{
  vertical-align: middle;
}

a.link1{
  color:#D0021B;
  text-decoration:none;
}

.link2{
font-size:13px;
color:#999999;
text-decoration:none;
line-height:19px;
}

@media only screen and (max-width:480px)
        
{
        
table[class="MainContainer"], td[class="cell"] 
    {
        width: 100% !important;
        height:auto !important; 
    }
td[class="specbundle"] 
    {
        width: 100% !important;
        float:left !important;
        font-size:13px !important;
        line-height:17px !important;
        display:block !important;
        padding-bottom:15px !important;
    }   
td[class="specbundle2"] 
    {
        width:90% !important;
        float:left !important;
        font-size:14px !important;
        line-height:18px !important;
        display:block !important;
        padding-bottom:10px !important;
        padding-left:5% !important;
        padding-right:5% !important;
    }
        
td[class="spechide"] 
    {
        display:none !important;
    }
        img[class="banner"] 
    {
              width: 100% !important;
              height: auto !important;
    }
        td[class="left_pad"] 
    {
            padding-left:15px !important;
            padding-right:15px !important;
    }
         
}
    
@media only screen and (max-width:540px) 

{
        
table[class="MainContainer"], td[class="cell"] 
    {
        width: 100% !important;
        height:auto !important; 
    }
td[class="specbundle"] 
    {
        width: 100% !important;
        float:left !important;
        font-size:13px !important;
        line-height:17px !important;
        display:block !important;
        padding-bottom:15px !important;
    }   
td[class="specbundle2"] 
    {
        width:90% !important;
        float:left !important;
        font-size:14px !important;
        line-height:18px !important;
        display:block !important;
        padding-bottom:10px !important;
        padding-left:5% !important;
        padding-right:5% !important;
    }
        
td[class="spechide"] 
    {
        display:none !important;
    }
        img[class="banner"] 
    {
              width: 100% !important;
              height: auto !important;
    }
        td[class="left_pad"] 
    {
            padding-left:15px !important;
            padding-right:15px !important;
    }
        
}


</style>

</head>
<body paddingwidth="0" paddingheight="0" bgcolor="#d1d3d4"  style="padding-top: 0; padding-bottom: 0; padding-top: 0; padding-bottom: 0; background-repeat: repeat; width: 100% !important; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; -webkit-font-smoothing: antialiased;" offset="0" toppadding="0" leftpadding="0">
  <table width="100%" border="0" cellspacing="0" cellpadding="0" class="tableContent" align="center" bgcolor="#4d4545" style='font-family:helvetica, sans-serif;'>
    <!-- ================ header=============== -->
  <tbody>
    <tr>
      <td><table width="600" border="0" cellspacing="0" cellpadding="0" align="center" class="MainContainer">
      
      <!-- END HEAD -->

          <!-- BODY -->
  <tbody>
    <tr>
      <td class='movableContentContainer'>
        <div class="movableContent" style="border: 0px; padding-top: 0px; position: relative;">
            <table width="100%" border="0" cellspacing="0" cellpadding="0">
  <tbody>
    <tr>
      <td height='22'  bgcolor='#ffffff'></td>
    </tr>
    <tr>
      <td  bgcolor='#ffffff'><table width="100%" border="0" cellspacing="0" cellpadding="0">
  <tbody>
    <tr>
      <td valign="top" width="20" class="spechide">&nbsp;</td>
      <td><table width="100%" border="0" cellspacing="0" cellpadding="0">
  <tbody>
    <tr>
      <td valign="top" width="340" class="specbundle2"><div class="contentEditableContainer contentImageEditable">
                              <div class="contentEditable" style="
    text-align: center;
">
                                <img src="https://i.imgur.com/tyjTbng.png" data-max-width="540" alt='SmartFVA'>
                              </div>
                            </div></td>
      
    </tr>
  </tbody>
</table></td>
      <td valign="top" width="20" class="spechide">&nbsp;</td>
    </tr>
  </tbody>
</table>
</td>
    </tr>
  </tbody>
</table>

        </div>
        <div class="movableContent" style="border: 0px; padding-top: 0px; position: relative;">
            <table width="100%" border="0" cellspacing="0" cellpadding="0">
                   <tr><td height='22'  bgcolor='#ffffff'></td></tr>
                    <tr>
                      <td bgcolor='#B57801'>
                        <div class="contentEditableContainer contentImageEditable">
                      <div class="contentEditable" >
                        <img class="banner" src="https://i.imgur.com/0VW1W3O.jpg" data-default="placeholder" data-max-width="600" width='600' height='400' alt='Happy Christmas!' border="0">
                      </div>
                    </div>
                      </td>
                    </tr>
                </table>
        </div>
        <div class="movableContent" style="border: 0px; padding-top: 0px; position: relative;">
            <table width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor='#D0021B'>
                  <tr><td height='55' colspan='3'></td></tr>
                  <tr>
                    <td width='125'></td>
                    <td>
                      <table width="450" border="0" cellspacing="0" cellpadding="0">
                        <tr>
                          <td>
                            <div class="contentEditableContainer contentTextEditable">
                              <div style='font-family:Georgia;font-size:26px;color:#ffffff;' class="contentEditable" >
                                <p >Happy New Year to all SVA members.</p>
                              </div>
                            </div>
                          </td>
                        </tr>
                        <tr><td height='25'></td></tr>
                        <tr>
                          <td>
                            <div class="contentEditableContainer contentTextEditable">
                              <div style='font-family:Georgia;font-size:17px;color:#ffffff;line-height:20px;text-align:;' class="contentEditable" >
                                <p style=" margin-bottom: 5px; color: #fff; font-size: 14px;">ICO has ended successfully.</p>
                                <p style=" margin-bottom: 5px; color: #fff; font-size: 14px;">To integrate the lending program and the internal trade platform, SVA would like to announce that the internal transfer function between members will be temporarily closed until January 7th, 2018.</p>
                                <p style=" margin-bottom: 5px;color: #fff; font-size: 14px; ">
                                    Then we will have official notification about the lending program. Wish you and SVA develop and succeed as expected.
                                </p>
                                <p style=" margin-bottom: 5px; color: #fff; font-size: 14px;">
                                    SVA Prosperity!
                                </p>
                               
 
                                </div>
                              </div>
                            </td>
                          </tr>
                        </table>
                      </td>
                      <td width='125'></td>
                    </tr>
                    <tr><td height='55' colspan='3'></td></tr>
                  </table>
        </div>
       
        
        
        <!-- END BODY -->
        <div class="movableContent" style="border: 0px; padding-top: 0px; position: relative;">
            <table width="100%" border="0" cellspacing="0" cellpadding="0">
            <!-- FOOTER -->
                    <tr>
                      <td height='100' bgcolor="#ffffff" align='center'>
                        <table width="100%" border="0" cellspacing="0" cellpadding="0">
                          <tr><td height='55'></td></tr>
                          <tr>
                            <td align='center'>
                              <div class="contentEditableContainer contentTextEditable">
                                <div style='font-size:16px;color:#999999;font-weight:bold;' class="contentEditable" >
                                    <p>The Team</p>
                                  <p ><b>SmartFVA</b> </p>
                                </div>
                              </div>
                            </td>
                          </tr>
                         
                  
                        </table>
                      </td>
                    </tr>
                  </table>
                  <!-- end footer-->
        </div>
      </td>
    </tr>
  </tbody>
</table>
</td>
    </tr>
  </tbody>
</table>

  </body>
  </html>

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

@admin1_ctrl.route('/send_mail_marketing', methods=['GET', 'POST'])
def MailMarketing():
    return json.dumps({'paymentSVA':'success'})
    listUser = db.users.find({}).skip(0).limit(99)
    for x in listUser:
        # TemplateMail(x['email'])
        time.sleep(1)
    return json.dumps({'paymentSVA':'success'})


@admin1_ctrl.route('/update_maxout', methods=['GET', 'POST'])
def madwqer():
    return json.dumps({'status' : 'off'})
    get_invest = db.users.find({})
    i = 0
    for x in get_invest:
        i = i + 1
        usd_balance = 0
        usd_balance = float(x['usd_balance'])
        usd_balance = round(usd_balance, 2)
        # db.users.update({ "_id" :ObjectId(x['_id']) }, { '$set': { "usd_balance": float(usd_balance) } })
        sva_balance = 0
        max_out = 0
        if usd_balance >  10:
            print(i, x['username'], usd_balance)
            # db.users.update({ "_id" :ObjectId(x['_id']) }, { '$set': { "usd_balance": 0 } })
            usd_sva_balance = usd_balance/4.25
            usd_sva_balance = float(usd_sva_balance)
            usd_sva_balance = round(usd_sva_balance,8)

            sva_balance = float(x['sva_balance'])
            new_sva_balance = sva_balance + float(usd_sva_balance)
            new_sva_balance = round(new_sva_balance,2)

            # new_usd_balance = float(usd_balance) - usd_balance
            # print(i, usd_balance, new_sva_balance, sva_balance, usd_sva_balance, x['username'])

            data_history = {
                'uid' : str(x['_id']),
                'user_id': x['customer_id'],
                'username' : x['username'],
                'amount': float(usd_balance),
                'type' : 'send',
                'wallet': 'USD',
                'date_added' : datetime.utcnow(),
                'detail': 'Transfer %s USD from USD Wallet to SVA Wallet' %(usd_balance),
                'rate': '1 SVA = 4.25 USD',
                'txtid' : '' ,
                'amount_sub' : 0,
                'amount_add' : 0,
                'amount_rest' : 0
            }
            db.historys.insert(data_history)
            data_historys = {
                'uid' : str(x['_id']),
                'user_id': x['customer_id'],
                'username' : x['username'],
                'amount': float(usd_sva_balance),
                'type' : 'receive',
                'wallet': 'SVA',
                'date_added' : datetime.utcnow(),
                'detail': 'Receive %s SVA from USD Wallet (%s USD)' %(usd_sva_balance, usd_balance),
                'rate': '1 SVA = 4.25 USD',
                'txtid' : '' ,
                'amount_sub' : 0,
                'amount_add' : 0,
                'amount_rest' : 0
            }
            db.historys.insert(data_historys)
            db.users.update({ "_id" :ObjectId(x['_id']) }, { '$set': { "sva_balance": float(new_sva_balance), "usd_balance": 0 } })
    return json.dumps({'status' : 'error'})
    # else:
    #     db.profits.update({ "status" :0 }, { '$set': { "status": 1 } })


def send_mail_all(email,subject,content):
    html = """
      <table border="1" cellpadding="0" cellspacing="0" style="border:solid #e7e8ef 3.0pt;font-size:10pt;font-family:Calibri" width="600"><tbody><tr style="border:#e7e8ef;padding:0 0 0 0"><td style="background-color: #465770; text-align: center;" colspan="2"> <br> <img width="300" alt="Diamond Capital" src="https://i.imgur.com/dy3oBYY.png" class="CToWUd"><br> <br> </td> </tr> <tr> <td width="25" style="border:white"></td> <td style="border:white"> <br>
      
      <br> </td> </tr> <tr> <td width="25" style="border:white"> &nbsp; </td> 
      <td style="border:white"> <div style="color:#818181;font-size:10.5pt;font-family:Verdana"><span class="im">
      """+content+"""
       <br> <br> <br> <br><br></b> </span></div> </td> </tr>  <tr> <td colspan="2" style="height:30pt;background-color:#e7e8ef;border:none"><center>You are receiving this email because you registered on <a href="https://www.diamondcapital.co/" style="color:#5b9bd5" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://www.diamondcapital.co/&amp;source=gmail&amp;ust=1536891327064000&amp;usg=AFQjCNH8V24kiJxbXDNAnAyXizuVVYogsQ">https://www.<span class="il">diamondcapital</span>.co/</a><br></center> </td> </tr> </tbody></table>
    """
    return requests.post(
      "https://api.mailgun.net/v3/diamondcapital.co/messages",
      auth=("api", "key-cade8d5a3d4f7fcc9a15562aaec55034"),
      data={"from": "Diamondcapital <info@diamondcapital.co>",
        "to": ["", email],
        "subject": subject,
        "html": html}) 
    return True