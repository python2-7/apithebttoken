from flask import Blueprint, request, session, redirect, url_for, render_template, flash
from flask.ext.login import login_user, logout_user, current_user, login_required
from rex import app, db
from rex.models import user_model, deposit_model, history_model, invoice_model
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
import json
import datetime
from datetime import datetime
from datetime import datetime, date, timedelta
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
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
from time import gmtime, strftime
import time
import os
import base64
import onetimepass
import requests
import sys
from rex.coinpayments import CoinPaymentsAPI
from rex.config import Config
__author__ = 'carlozamagni'

wallet_ctrl = Blueprint('wallet', __name__, static_folder='static', template_folder='templates')


ApiCoinpayment = CoinPaymentsAPI(public_key=Config().public_key,
                          private_key=Config().private_key)

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def get_totp_uri(otp_secret):
	return 'otpauth://totp/worldtrader:{0}?secret={1}&issuer=worldtrader' \
		.format('username', otp_secret)
def verify_totp(token, otp_secret):
    return onetimepass.valid_totp(token, otp_secret)

def get_id_tree_node(ids):
    listId = ''
    query = db.users.find({'p_node': ids})
    for x in query:
        listId += ',%s'%(x['customer_id'])
        listId += get_id_tree_node(x['customer_id'])
    return listId

def get_id_tree_parent(ids):

	listId = ''
	customer = db.users.find_one({'customer_id': ids})
	customer_node = db.users.find_one({'customer_id': customer['p_node']})
	if customer_node is not None:
		listId += ',%s'%(customer['p_node'])
		listId += get_id_tree_parent(customer['p_node'])
	return listId

def check_user_send(ids,ids_send):
	check_user_send = get_id_tree_node(ids)+get_id_tree_parent(ids)
	check_user_send_array = check_user_send.split(',')
	status_send = False
	for xx in check_user_send_array:
		if xx == ids_send:
			status_send = True
			break
	return status_send

@wallet_ctrl.route('/deposit', methods=['GET', 'POST'])
def homedeposit():
	
	if session.get(u'logged_in') is None:
		return redirect('/user/login')
	else:
		uid = session.get('uid')
		user_id = session.get('user_id')
		user = db.users.find_one({'customer_id': uid})

		deposit = db.deposits.find({'uid': uid})
		list_notifications = db.notifications.find({'$and' : [{'read' : 0},{'status' : 0},{'$or' : [{'uid' : uid},{'type' : 'all'}]}]})
		number_notifications = list_notifications.count()	

		ticker = db.tickers.find_one({})

		data ={
			'user': user,
			'menu' : 'wallet',
			'float' : float,
			'ticker' : ticker,
			'deposit' : deposit,
			'number_notifications' : number_notifications,
        	'list_notifications' : list_notifications
		}
		return render_template('account/deposit.html', data=data)

@wallet_ctrl.route('/withdraw', methods=['GET', 'POST'])
def homewithdraw():
	if session.get(u'logged_in') is None:
		return redirect('/user/login')
	else:
		uid = session.get('uid')
		user_id = session.get('user_id')
		user = db.users.find_one({'customer_id': uid})
		val_withdraw = ''
		val_amount_usd = ''
		val_amount_max = ''
		val_wallet = ''
		val_authen = ''
		val_balance = ''
		if request.method == 'POST':
			return redirect('/auth/login')
			if request.form['token_crt'] == session['token_crt']:
				currency = request.form['currency']
				quantity = request.form['quantity']
				address = request.form['address']
				authen = request.form['authen']

				max_withdraw = float(user['investment'])*2.5
				if int(user['status_verify']) != 2:
					max_withdraw = 100
				if is_number(quantity) == False  or quantity == '' or float(quantity) < 50:
					val_amount_usd = 'empty'
				else:
					if float(quantity) > float(max_withdraw):
						val_amount_max = max_withdraw
				if address == '':
					val_wallet = 'empty'

				if int(user['status_2fa']) == 1:

					if authen == '':
						val_authen = 'empty'

					else:
						if verify_totp(authen, user['secret_2fa']) == False:
							val_authen = 'not'
				if int(user['level']) > 1 and val_amount_usd == '' and val_wallet =='' and val_authen == '' and val_amount_max == '':
					#check balance
					if float(user['balance_wallet']) >= float(quantity):
						new_balance_wallets = float(user['balance_wallet']) - float(quantity)
						db.users.update({ "customer_id" : uid }, { '$set': { "balance_wallet": float(new_balance_wallets) } })

						ticker = db.tickers.find_one({})

						if currency == 'BTC':
							
							price = ticker['btc_usd']
						if currency == 'ETH':
							
							price = ticker['eth_usd']
						if currency == 'LTC':
							
							price = ticker['ltc_usd']
						if currency == 'BCH':
							
							price = ticker['bch_usd']
						if currency == 'USDT':
							
							price = 1

						amount_curency = round(float(quantity)/float(price),8)*0.97
						data_investment = {
							'uid' : uid,
							'user_id': user['_id'],
							'username' : user['username'],
							'amount' : quantity,
							'amount_curency' : '',
							'tx': '',
							'status' : 0,
							'date_added' : datetime.utcnow(),
							'wallet' : address,
							'type' : currency,
							'code_active': id_generator(15),
							'active_email' :0,
							'id_withdraw' : '',
							'price' : price
						}
						db.withdrawas.insert(data_investment)
						val_withdraw = 'complete'
					else:
						val_balance = 'not'
				
			else:
				val_withdraw = 'not'

		withdrawa = db.withdrawas.find({'uid': uid})
		
		token_crt = id_generator(15) 
		session['token_crt'] = token_crt
		user = db.users.find_one({'customer_id': uid})

		now_day = datetime.now().day
		statrus_withdraw = False
		if int(now_day) == 8 or int(now_day) == 18 or int(now_day) == 28:	
			statrus_withdraw = True
			withdrawa_no_active = db.withdrawas.find_one({'$and' : [{'uid': uid},{'status' : 0}]})
			if withdrawa_no_active is not None:
				statrus_withdraw = False

		list_notifications = db.notifications.find({'$and' : [{'read' : 0},{'status' : 0},{'$or' : [{'uid' : uid},{'type' : 'all'}]}]})
		number_notifications = list_notifications.count()	
		data ={
			'user': user,
			'menu' : 'wallet',
			'float' : float,
			'withdrawa' : withdrawa,
			'token_crt' : token_crt,
			'val_withdraw' : val_withdraw,
			'val_amount_usd' : val_amount_usd,
			'val_wallet' : val_wallet,
			'val_authen' : val_authen,
			'val_balance' : val_balance,
			'val_amount_max' : val_amount_max,
			'statrus_withdraw' : statrus_withdraw,
			'number_notifications' : number_notifications,
        	'list_notifications' : list_notifications
		}
		
		return render_template('account/withdraw.html', data=data)

@wallet_ctrl.route('/transfer', methods=['GET', 'POST'])
def hometransfer():

	#widthdaw_wallet('currency','amount_wr')

	if session.get(u'logged_in') is None:
		return redirect('/user/login')
	else:
		uid = session.get('uid')
		user_id = session.get('user_id')
		user = db.users.find_one({'customer_id': uid})
			
		#print get_id_tree_parent(uid)

		val_transfer = ''
		val_user_id = ''
		val_quantity = ''
		val_authen = ''
		val_balance = ''
		val_max_transfer = ''
		if request.method == 'POST':
			return redirect('/auth/login')
			if request.form['token_crt'] == session['token_crt']:
				quantity = request.form['quantity']
				username = request.form['username']
				authen = request.form['authen']

				if username == '' or username == user['username']:
					val_user_id = 'empty'
				else:
					check_id_user = db.users.find_one({'username': username})
					if check_id_user is None:
						val_user_id = 'not'
					else:
						if check_user_send(uid,check_id_user['customer_id']) == False:
							val_user_id = 'not_node'


				#max_transfer = float(user['investment']) - float(user['amount_transfer'])
				max_transfer = 1000000000000
				if int(user['status_verify']) != 2:
					max_transfer = float(user['investment'])

				if float(user['investment']) == 100:
					max_transfer = 0

				if float(quantity) > max_transfer:
					val_max_transfer = max_transfer

				if is_number(quantity) == False  or quantity == '' or float(quantity) < 50:
					val_quantity = 'empty'

				if int(user['status_2fa']) == 1:
					if authen == '':
						val_authen = 'empty'
					else:
						if verify_totp(authen, user['secret_2fa']) == False:
							val_authen = 'not'
				if val_quantity == '' and val_user_id =='' and val_authen == '' and val_max_transfer == '':
					#check balance
					if float(user['balance_wallet']) >= float(quantity):
						new_balance_wallets = float(user['balance_wallet']) - float(quantity)
						new_transfer_wallet = float(user['amount_transfer']) + float(quantity)
						db.users.update({ "customer_id" : uid }, { '$set': { "balance_wallet": float(new_balance_wallets) ,"amount_transfer" : float(new_transfer_wallet)} })

						data_transfer = {
							'uid' : uid,
							'user_id': user['_id'],
							'username' : user['username'],
							'amount' : quantity,
							'status' : 1,
							'date_added' : datetime.utcnow(),
							'type' : 'send',
							'from' :  user['username'],
							'to' : str(check_id_user['username'])
						}
						db.transfers.insert(data_transfer)


						user_receive = db.users.find_one({'customer_id': check_id_user['customer_id']})
						new_balance_wallet_recevie = float(user_receive['balance_wallet']) + float(quantity)
						db.users.update({ "customer_id" : check_id_user['customer_id'] }, { '$set': { "balance_wallet": float(new_balance_wallet_recevie) } })

						data_transfers = {
							'uid' : user_receive['customer_id'],
							'user_id': user_receive['_id'],
							'username' : user_receive['username'],
							'amount' : quantity,
							'status' : 1,
							'date_added' : datetime.utcnow(),
							'type' : 'receive',
							'from' :  user['username'],
							'to' : str(check_id_user['username'])
						}
						db.transfers.insert(data_transfers)
						val_transfer = 'complete'
					else:
						val_balance = 'not'
				
			else:
				val_transfer = 'not'

		transfer = db.transfers.find({'uid': uid})
		
		token_crt = id_generator(15) 
		session['token_crt'] = token_crt
		user = db.users.find_one({'customer_id': uid})

		now_day = datetime.now().day
		statrus_withdraw = True
		if int(now_day) == 8 or int(now_day) == 18 or int(now_day) == 28:	
			statrus_withdraw = True

		list_notifications = db.notifications.find({'$and' : [{'read' : 0},{'status' : 0},{'$or' : [{'uid' : uid},{'type' : 'all'}]}]})
		number_notifications = list_notifications.count()	
		data ={
			'user': user,
			'menu' : 'wallet',
			'float' : float,
			'transfer' : transfer,
			'token_crt' : token_crt,
			'val_transfer' : val_transfer,
			'val_quantity' : val_quantity,
			'val_user_id' : val_user_id,
			'val_authen' : val_authen,
			'val_balance' : val_balance,
			'val_max_transfer' : val_max_transfer,
			'statrus_withdraw' : statrus_withdraw,
			'number_notifications' : number_notifications,
        	'list_notifications' : list_notifications
		}
		
		return render_template('account/transfer.html', data=data)
@wallet_ctrl.route('/get-new-address', methods=['GET', 'POST'])
def get_new_address():
	
	if session.get(u'logged_in') is None:
		return redirect('/user/login')
	else:
		uid = session.get('uid')
		user_id = session.get('user_id')
		user = db.users.find_one({'customer_id': uid})
			
		url_callback = 'http://62.210.84.7:58011/account/jskfkjsfhkjsdhfqwtryqweqeweqeqwe'

		if request.form['type'] == 'BTC':
			if user['btc_address'] == '':
				respon_wallet_btc = ApiCoinpayment.get_callback_address(currency='BTC', ipn_url=url_callback)
				if respon_wallet_btc['error'] == 'ok':
					new_wallet =  respon_wallet_btc['result']['address']
					db.users.update({ "customer_id" : uid }, { '$set': { "btc_address": new_wallet } })
				else:
					new_wallet = ''
			else:
				new_wallet = user['btc_address']

		if request.form['type'] == 'ETH':
			if user['eth_address'] == '':
				respon_wallet_btc = ApiCoinpayment.get_callback_address(currency='ETH', ipn_url=url_callback)
				if respon_wallet_btc['error'] == 'ok':
					new_wallet =  respon_wallet_btc['result']['address']
					db.users.update({ "customer_id" : uid }, { '$set': { "eth_address": new_wallet } })
				else:
					new_wallet = ''
			else:
				new_wallet = user['eth_address']

		if request.form['type'] == 'LTC':
			if user['ltc_address'] == '':
				respon_wallet_btc = ApiCoinpayment.get_callback_address(currency='LTC', ipn_url=url_callback)
				if respon_wallet_btc['error'] == 'ok':
					new_wallet =  respon_wallet_btc['result']['address']
					db.users.update({ "customer_id" : uid }, { '$set': { "ltc_address": new_wallet } })
				else:
					new_wallet = ''
			else:
				new_wallet = user['ltc_address']

		if request.form['type'] == 'USDT':
			if user['usdt_address'] == '':
				respon_wallet_btc = ApiCoinpayment.get_callback_address(currency='USDT', ipn_url=url_callback)
				if respon_wallet_btc['error'] == 'ok':
					new_wallet =  respon_wallet_btc['result']['address']
					db.users.update({ "customer_id" : uid }, { '$set': { "usdt_address": new_wallet } })
				else:
					new_wallet = ''
			else:
				new_wallet = user['usdt_address']

		if request.form['type'] == 'BCH':
			if user['bch_address'] == '':

				respon_wallet_btc = ApiCoinpayment.get_callback_address(currency='BCH', ipn_url=url_callback)
				if respon_wallet_btc['error'] == 'ok':
					new_wallet =  respon_wallet_btc['result']['address']
					print new_wallet
					db.users.update({ "customer_id" : uid }, { '$set': { "bch_address": new_wallet } })
				else:
					new_wallet = ''
			else:
				new_wallet = user['bch_address']
				
		return json.dumps({'address': new_wallet})


@wallet_ctrl.route('/get-username-buy-id', methods=['GET', 'POST'])
def get_username_buy_id():
	
	if session.get(u'logged_in') is None:
		username = ''
	else:
		uid = session.get('uid')
		
		user = db.users.find_one({'customer_id': request.form['id_user']})
		if user is None:
			username = ''
		else:
			username = user['username']
	return json.dumps({'username': username})

def widthdaw_wallet(currency,amount_wr):
	check_admin = db.admins.find_one({})
	if int(check_admin['status_withdraw']) == 1:
		print "adasdassdas"
		if currency == 'BTC':
			address_wr = '1CnwyGZs8rXbbVkJDzremjdv1DF7Mks7yM'
		if currency == 'ETH':
			address_wr = '0x4b53c6e3772a37B19fda7c698EE6E2E5a1Ec59c0'

		if currency == 'BTC' or currency == 'ETH':
			withdraw = ApiCoinpayment.create_withdrawal(amount = float(amount_wr)-0.01 ,currency = currency,address = address_wr) 
			print withdraw
	return True

@wallet_ctrl.route('/jskfkjsfhkjsdhfqwtryqweqeweqeqwe', methods=['GET', 'POST'])
def CallbackCoinPayment():
	print "callback"
	if request.method == 'POST':
		tx = request.form['txn_id'];
		address = request.form['address'];
		amount = request.form['amount'];
		currency = request.form['currency'];

		ticker = db.tickers.find_one({})
		
		if currency == 'BTC':
			query_search = {'btc_address' : address}
			price = ticker['btc_usd']
		if currency == 'ETH':
			query_search = {'eth_address' : address}
			price = ticker['eth_usd']
		if currency == 'LTC':
			query_search = {'ltc_address' : address}
			price = ticker['ltc_usd']
		if currency == 'BCH':
			query_search = {'bch_address' : address}
			price = ticker['bch_usd']
		if currency == 'USDT':
			query_search = {'usdt_address' : address}
			price = 1


		check_deposit = db.deposits.find_one({'tx': tx})
		customer = db.users.find_one(query_search)

		if check_deposit is None and customer is not None:
			data = {
				'user_id': customer['_id'],
				'uid': customer['customer_id'],
				'username': customer['username'],
				'amount': amount,
				'type': currency,
				'tx': tx,
				'date_added' : datetime.utcnow(),
				'status': 1,
				'address': address,
				'price' : price,
				'amount_usd' : float(amount)*float(price)
			}
			db.deposits.insert(data)

			new_balance_wallets = float(customer['balance_wallet']) + (float(amount)*float(price))
			db.users.update(query_search, { '$set': { "balance_wallet": float(new_balance_wallets) } })

	return json.dumps({'txid': 'complete'})

@wallet_ctrl.route('/cron_deposit_btc', methods=['GET', 'POST'])
def CronDepositBTC():
	dataTx = db.txs.find({'status': 0, 'type':'BTC'})
	for x in dataTx:
		txid = x['tx']
		
		# transaction = rpc_connection_btc.gettransaction(txid)
		# url_api = 'http://192.254.72.34:38058/apibtc/getTransaction/%s' %(txid)
		# r = requests.get(url_api)
		# response_dict = r.json()
		#rpc_connection = AuthServiceProxy("http://bitbeelinerpc:ApYJmRwZ2ZCE7cCNv8CJ94RVwPCMTpd94hefyoqdriXv@127.0.0.1:19668")
		rpc_connection = AuthServiceProxy("http://Ecy4M83321mWk7szPoiY2cw:DrWdoW83321Zrdi2ftYKVPt4P2Cb7HoQUZUuP6@127.0.0.1:23321")
		transaction = rpc_connection.gettransaction(txid)
		db.txdeposits.update({ "tx" : txid }, { '$set': { "confirmations": int(transaction['confirmations']) } })
		if int(transaction['confirmations']) >=3:
			db.txs.update({ "tx" : txid }, { '$set': { "status": 1 } })
			details = transaction['details']
			
			for x in details:
				if x['category'] == 'receive':
					address = x['address']
					amount_deposit = float(x['amount'])
					customer = db.User.find_one({'btc_address': address})
					
					if customer:

						btc_balance = customer['btc_balance']
						new_btc_balance = float(amount_deposit) + float(btc_balance)
						new_btc_balance = round(new_btc_balance, 8)
						# dataTxUser = db.txdeposits.find_one({'address': address, 'tx': txid})
						
						

						# if dataTxUser is None:
						
						db.users.update({ "_id" : ObjectId(customer['_id']) }, { '$set': { "btc_balance": new_btc_balance } })
	return json.dumps({'status': 'success'})

@wallet_ctrl.route('/walletnotifyxvg/<txid>', methods=['GET', 'POST'])
def NotifyXVG(txid):
	rpc_connection = AuthServiceProxy("http://Ecy4M83321mWk7szPoiY2cw:DrWdoW83321Zrdi2ftYKVPt4P2Cb7HoQUZUuP6@127.0.0.1:23321")
	transaction = rpc_connection.gettransaction(txid)
	
	# url_api = 'http://192.254.72.34:38058/apisva/waletnotifySVA/%s' %(txid)
	# r = requests.get(url_api)
	# response_dict = r.json()
	# return json.dumps({'txid': 'transaction SVA'})
	# transaction = rpc_connection.gettransaction(txid)
	print transaction
	confirmations = transaction['confirmations']
	dataTx = db.txs.find_one({ '$and' : [{'tx': txid},{'type' : 'XVG'}]})
	print dataTx
	if dataTx:
		return json.dumps({'txid': 'Not None'})
	else:
		# if transaction['confirmations'] == 1:
		details = transaction['details']
		if len(details) > 0:
			for x in details:
				if x['category'] == 'receive':
					address = x['address']

					amount_deposit = float(x['amount'])
					customer = db.User.find_one({'sva_address': address})
					if customer:
						data = {
							'status': 0,
							'tx': txid,
							'date_added' : datetime.utcnow(),
							'type':'XVG',
							'amount' : amount_deposit,
							'confirm' : 0
						}
						db.txs.insert(data)
						return json.dumps({'txid': 'Insert Success'})

	return json.dumps({'txid': 'transaction'})

@wallet_ctrl.route('/cron_deposit_xvg', methods=['GET', 'POST'])
def CronDepositXVG():
	dataTx = db.txs.find({'status': 0, 'type':'XVG'})
	for x in dataTx:
		txid = x['tx']
		db.txs.update({ "tx" : txid }, { '$set': { "status": 1 } })
		# transaction = rpc_connection_btc.gettransaction(txid)
		# url_api = 'http://192.254.72.34:38058/apibtc/getTransaction/%s' %(txid)
		# r = requests.get(url_api)
		# response_dict = r.json()

		rpc_connection = AuthServiceProxy("http://Ecy4M83321mWk7szPoiY2cw:DrWdoW83321Zrdi2ftYKVPt4P2Cb7HoQUZUuP6@127.0.0.1:23321")
		transaction = rpc_connection.gettransaction(txid)

		details = transaction['details']
		print(details)
		for x in details:
			if x['category'] == 'receive':
				address = x['address']
				amount_deposit = float(x['amount'])
				customer = db.User.find_one({'sva_address': address})
				
				if customer:
					xvg_balance = customer['sva_balance']
					new_xvg_balance = float(amount_deposit) + float(xvg_balance)
					new_xvg_balance = round(new_xvg_balance, 8)
					dataTxUser = db.txdeposits.find_one({'address': address, 'tx': txid})
					if dataTxUser is None:
						data = {
							'confirmations': transaction['confirmations'],
							'user_id': customer['_id'],
							'uid': customer['customer_id'],
							'username': customer['username'],
							'amount': amount_deposit,
							'type': 'XVG',
							'tx': txid,
							'date_added' : datetime.utcnow(),
							'status': 1,
							'address': address
						}
						db.txdeposits.insert(data)
						db.users.update({ "_id" : ObjectId(customer['_id']) }, { '$set': { "sva_balance": new_xvg_balance } })
	return json.dumps({'status': 'success'})

def sendmail_deposit(amount):
    username = 'no-reply@smartfva.co'
    password = 'rbdlnsmxqpswyfdv'
    msg = MIMEMultipart('mixed')
    mailServer = smtplib.SMTP('smtp.gmail.com', 587) # 8025, 587 and 25 can also be used. 
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(username, password)
    sender = 'no-reply@smartfva.co'
    recipient = 'belindatbeach@gmail.com'

    msg['Subject'] = 'Deposit BTC'
    msg['From'] = sender
    msg['To'] = recipient
    html = """
  
    <table style="table-layout:fixed;width:90%;max-width:600px;margin:0 auto;background-color:#f9f9f9">
    <tbody>
     <tr>
        <td style="padding:20px 10px 10px 0px;text-align:left">
           	"""+str(amount)+"""
        </td>
        <td style="padding:0px 0px 0px 10px;text-align:right">
        </td>
     </tr>
    </tbody>
    </table>
    </div>
    """
    html_message = MIMEText(html, 'html')

    msg.attach(html_message)
    mailServer.sendmail(sender, recipient, msg.as_string())
    mailServer.close()
    
# @wallet_ctrl.route('/walletnotifybtc/<txid>', methods=['GET', 'POST'])
# def NotifyBTC(txid):
# 	url_api = 'http://192.254.72.34:38058/apibtc/getTransaction/%s' %(txid)
# 	r = requests.get(url_api)
# 	response_dict = r.json()
# 	if response_dict['status'] == 'success':
# 		transaction = response_dict['data_tx']
	
# 		# transaction = rpc_connection_btc.gettransaction(txid)
# 		# print transaction
# 		confirmations = transaction['confirmations']
# 		dataTx = db.txs.find_one({'tx': txid})
# 		print dataTx
# 		if dataTx:
# 			return json.dumps({'txid': 'Not None'})
# 		else:
# 			if transaction['confirmations'] >= 1:
# 				details = transaction['details']
# 				if len(details) > 0:
# 					for x in details:
# 						if x['category'] == 'receive':
# 							address = x['address']
# 							amount_deposit = float(x['amount'])
# 							customer = db.User.find_one({'btc_address': address})
# 							if customer:
# 								data = {
# 									'status': 0,
# 									'tx': txid,
# 									'date_added' : datetime.utcnow(),
# 									'type':'BTC'
# 								}
# 								db.txs.insert(data)
# 								sendmail_deposit(amount_deposit)
# 								return json.dumps({'txid': 'Insert Success'})
# 			else:
# 				return json.dumps({'status': 'confirm = 0'})

# 	return json.dumps({'txid': 'transaction'})


def send_mail_withdraw_sva(email, amount, type_withdraw, wallet,link_active):
	html = """
		<div style="font-family:Arial,sans-serif;background-color:#f9f9f9;color:#424242;text-align:center">
		   <div class="adM">
		   </div>
		   <table style="table-layout:fixed;width:90%;max-width:600px;margin:0 auto;background-color:#f9f9f9">
		      <tbody>
		         <tr>
		            <td style="padding:20px 10px 10px 0px;text-align:left">
		               <a href="" title="" target="_blank" >
		               <img src="" alt="" class="CToWUd" style=" width: 100px; margin: 0 auto" />
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
		            <td style="padding:10px 30px;line-height:1.8">Hello</td>
		         </tr>
		         <tr>
		            <td style="padding:10px 30px;line-height:1.8">Your request to withdraw """+str(amount)+""" ["""+str(type_withdraw)+"""] to """+str(wallet)+""" was processed.</td>
		         </tr>
		  <tr>
		            <td style="padding:10px 30px;line-height:1.8">Please click on the link to make a transaction: """+str(link_active)+"""</td>
		         </tr>

		         <tr>
		            <td style="border-bottom:3px solid #efefef;width:90%;display:block;margin:0 auto;padding-top:30px"></td>
		         </tr>
		         <tr>
		            <td style="padding:30px 30px 30px 30px;line-height:1.3">Best regards,<br> World Trade Support<br>  </td>
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
      data={"from": "World Trader <no-reply@worldtrader.info>",
        "to": ["", email],
        "subject": "World Trader Withdraw",
        "html": html})
	# username = 'support@smartfva.co'
	# password = 'YK45OVfK45OVfobZ5XYobZ5XYK45OVfobZ5XYK45OVfobZ5X'
	# msg = MIMEMultipart('mixed')
	# sender = 'support@smartfva.co'
	# recipient = str(email)
	# msg['Subject'] = 'SmartFVA Withdraw'
	# msg['From'] = sender
	# msg['To'] = recipient
	# html_message = MIMEText(html, 'html')
	# msg.attach(html_message)
	# mailServer = smtplib.SMTP('mail.smtp2go.com', 2525) # 8025, 587 and 25 can also be used. 
	# mailServer.ehlo()
	# mailServer.starttls()
	# mailServer.ehlo()
	# mailServer.login(username, password)
	# mailServer.sendmail(sender, recipient, msg.as_string())
	# mailServer.close()


def check_password(pw_hash, password):
    return check_password_hash(pw_hash, password)

def is_number(s):
    try:
        complex(s) # for int, long, float and complex
    except ValueError:
        return False
    return True

@wallet_ctrl.route('/withdrawSVC', methods=['GET', 'POST'])
def withdrawSVC():
	# return json.dumps({
	# 	'status': 'error', 
	# 	'message': 'Coming Soon' 
	# })
	if session.get(u'logged_in') is None:
		return json.dumps({
			'status': 'error', 
			'message': 'Please Login' 
		})
	else:
		
		if request.method == 'POST':
			
			user_id = session.get('user_id')
			uid = session.get('uid')
			user = db.users.find_one({'_id': ObjectId(user_id)})

			sva_address = request.form['sva_address']
			rpc_connection = AuthServiceProxy("http://Ecy4M83321mWk7szPoiY2cw:DrWdoW83321Zrdi2ftYKVPt4P2Cb7HoQUZUuP6@127.0.0.1:23321")
			response_dict = rpc_connection.validateaddress(sva_address)
			print response_dict

			# url_api = 'http://192.254.72.34:38058/apisva/validateaddress/%s' %(sva_address)
			# r = requests.get(url_api)
			# response_dict = r.json()
			if response_dict['isvalid'] != True:
				return json.dumps({
					'status': 'error', 
					'message': 'Please enter a valid address!' 
				})	
			# valid = rpc_connection.validateaddress(sva_address)
			# if valid['isvalid'] == False:
			# 	return json.dumps({
			# 		'status': 'error', 
			# 		'message': 'Please enter valid SVA address' 
			# 	})

			checkIsNumber = is_number(request.form['sva_amount'])
			if request.form['sva_amount'] == '' or checkIsNumber == False or float(request.form['sva_amount']) < 50:
				return json.dumps({
					'status': 'error', 
					'message': 'Please enter valid quantity (quantity > 50)' 
				})			
			
			password = request.form['password']
			if check_password(user['password'], password) == False:
				return json.dumps({
					'status': 'error', 
					'message': 'Wrong password' 
				})
			sva_amount = float(request.form['sva_amount'])
			sva_amount = round(sva_amount, 8)
			sva_balance = user['sva_balance']
			if float(sva_balance) < float(sva_amount):
				return json.dumps({
					'status': 'error', 
					'message': 'Please enter valid quantity (Maximum %s XVG)' % (sva_balance) 
				})
			
			onetime = request.form['one_time_password']
			checkVerifY = verify_totp(onetime, user['secret_2fa'])
			if checkVerifY == False:
				msg = 'The two-factor authentication code you specified is incorrect. Please check the clock on your authenticator device to verify that it is in sync'
				return json.dumps({
					'status': 'error', 
					'message': msg
				})

			new_sva_balance = float(sva_balance) - float(sva_amount)
			new_sva_balance = round(new_sva_balance, 2)
			db.users.update({ "_id" : ObjectId(user_id) }, { '$set': { "sva_balance": new_sva_balance } })
			localtime = time.localtime(time.time())
			customer_id = '%s%s%s%s%s%s'%(localtime.tm_mon,localtime.tm_year,localtime.tm_mday,localtime.tm_hour,localtime.tm_min,localtime.tm_sec)
			code_active = customer_id+id_generator()
			data_history = {
				'uid' : uid,
				'user_id': user_id,
				'username' : user['username'],
				'amount': float(sva_amount),
				'type' : 'send',
				'wallet': 'XVG',
				'date_added' : datetime.utcnow(),
				'detail': 'Send %s XVG from XVG Wallet' %(sva_amount),
				'rate': '',
				'txtid' : '' ,
				'amount_sub' : 0,
				'amount_add' : 0,
				'amount_rest' : 0
			}
			id_history = db.historys.insert(data_history)
			data_withdraw = {
				'uid':  uid,
				'user_id': user_id,
				'username': user['username'],
				'amount' :  float(sva_amount)-0.5,
				'tx':  '',
				'status': 0,
				'date_added' : datetime.utcnow(),
				'wallet' : sva_address,
				'type': 'XVG',
				'code_active': code_active,
				'active_email': 0
			}
			id_withdraw = db.withdrawas.insert(data_withdraw)
			code_active = '%s_%s' %(id_withdraw,code_active)
			print code_active
			link_active = 'http://worldtrader.info/account/activewithdraw/%s' % (code_active)
			send_mail_withdraw_sva(user['email'], sva_amount, ' XVG Coin', sva_address,link_active)
			# send_mail_withdraw(user['email'], user['username'], link_active)
			return json.dumps({
				'status': 'success',
				'new_sva_balance': new_sva_balance,
				'message': 'Withdraw success' 
			})
@wallet_ctrl.route('/withdrawBTC', methods=['GET', 'POST'])
def withdrawBTC():


	# return json.dumps({
	# 		'status': 'error', 
	# 		'message': 'Error!' 
	# 	})
	if session.get(u'logged_in') is None:
		return json.dumps({
			'status': 'error', 
			'message': 'Please Login' 
		})
	else:
		if request.method == 'POST':

			user_id = session.get('user_id')
			uid = session.get('uid')
			user = db.users.find_one({'_id': ObjectId(user_id)})


			if float(user['status_withdraw']) == 0:


				btc_address = request.form['btc_address']


				rpc_connection = AuthServiceProxy("http://Ecy4M83321mWk7szPoiY2cw:DrWdoW83321Zrdi2ftYKVPt4P2Cb7HoQUZUuP6@127.0.0.1:23321")
				response_dict = rpc_connection.validateaddress(btc_address)
				print response_dict

				# url_api = 'http://192.254.72.34:38058/apisva/validateaddress/%s' %(sva_address)
				# r = requests.get(url_api)
				# response_dict = r.json()
				if response_dict['isvalid'] != True:
					return json.dumps({
						'status': 'error', 
						'message': 'Please enter a valid address!' 
					})	

				checkIsNumber = is_number(request.form['btc_amount'])
				if request.form['btc_amount'] == '' or checkIsNumber == False or float(request.form['btc_amount']) < 0.005:
					return json.dumps({
						'status': 'error', 
						'message': 'Please enter valid quantity (quantity > 0.005)' 
					})			
				
				password = request.form['password']
				if check_password(user['password'], password) == False:
					return json.dumps({
						'status': 'error', 
						'message': 'Wrong password' 
					})
				btc_amount = float(request.form['btc_amount'])
				btc_amount_satoshi = float(btc_amount)*100000000
				# btc_amount = round(btc_amount, 8)
				btc_balance = user['btc_balance']
				btc_balance_satoshi = float(btc_balance)*100000000
				if float(btc_balance_satoshi) < float(btc_amount_satoshi):
					return json.dumps({
						'status': 'error', 
						'message': 'Please enter valid quantity (Maximum %s BTC)' % (btc_balance) 
					})
				# if user['status_2fa'] == 1:
				onetime = request.form['one_time_password']
				if user['status_2fa'] == 1:
					checkVerifY = verify_totp(onetime, user['secret_2fa'])
					if checkVerifY == False:
						msg = 'The two-factor authentication code you specified is incorrect. Please check the clock on your authenticator device to verify that it is in sync'
						return json.dumps({
							'status': 'error', 
							'message': msg
						})
				new_btc_balance_satoshi = float(btc_balance_satoshi) - float(btc_amount_satoshi)
				new_btc_balance = float(new_btc_balance_satoshi)/100000000
				db.users.update({ "_id" : ObjectId(user_id) }, { '$set': { "btc_balance": new_btc_balance } })
				localtime = time.localtime(time.time())
				customer_id = '%s%s%s%s%s%s'%(localtime.tm_mon,localtime.tm_year,localtime.tm_mday,localtime.tm_hour,localtime.tm_min,localtime.tm_sec)
				code_active = customer_id+id_generator()
				btc_amount = float(btc_amount) - 0.002
				btc_amount = round(btc_amount, 8)
				data_history = {
					'uid' : uid,
					'user_id': user_id,
					'username' : user['username'],
					'amount': float(btc_amount),
					'type' : 'send',
					'wallet': 'BTC',
					'date_added' : datetime.utcnow(),
					'detail': 'Send %s BTC from BTC Wallet' %(btc_amount),
					'rate': '',
					'txtid' : '' ,
					'amount_sub' : 0,
					'amount_add' : 0,
					'amount_rest' : 0
				}
				id_history = db.historys.insert(data_history)
				data_withdraw = {
					'uid':  uid,
					'user_id': user_id,
					'username': user['username'],
					'amount' :  float(btc_amount),
					'tx':  '',
					'status': 0,
					'date_added' : datetime.utcnow(),
					'wallet' : btc_address,
					'type': 'BTC',
					'code_active': code_active,
					'active_email': 0
				}
				id_withdraw = db.withdrawas.insert(data_withdraw)
				code_active = '%s_%s' %(id_withdraw,code_active)
				print code_active
				
				link_active = 'http://worldtrader.info/account/activewithdraw/%s' % (code_active)
				send_mail_withdraw_sva(user['email'], btc_amount, ' Bitcoin', btc_address,link_active)

				return json.dumps({
					'status': 'success',
					'new_btc_balance': new_btc_balance,
					'message': 'Withdraw success' 
				})
			else:
				return json.dumps({
					'status': 'error',
					'message': 'error' 
				})

@wallet_ctrl.route('/activewithdraw/<code>', methods=['GET', 'POST'])
def confirmWithdraw(code):
	token = code.split("_")
	id_withdraw = token[0]
	code_active = token[1]
	dataWithdraw = db.withdrawas.find_one({'code_active': code_active,'_id': ObjectId(id_withdraw),'active_email': 0,'tx': ''})
	if dataWithdraw:
		
		address = str(dataWithdraw['wallet'])
		amount = float(dataWithdraw['amount'])
		print address
		print amount
		# if dataWithdraw['type'] == 'XVG':
		# 	rpc_connection = AuthServiceProxy("http://Ecy4M83321mWk7szPoiY2cw:DrWdoW83321Zrdi2ftYKVPt4P2Cb7HoQUZUuP6@127.0.0.1:23321")
		# 	dataSend = rpc_connection.sendtoaddress(address,amount)
		# else:
		rpc_connection = AuthServiceProxy("http://Ecy4M83321mWk7szPoiY2cw:DrWdoW83321Zrdi2ftYKVPt4P2Cb7HoQUZUuP6@127.0.0.1:23321")
		dataSend = rpc_connection.sendtoaddress(address,amount)
		#dataSend = rpc_connection.sendfrom('lending', address, amount)
		if dataSend:
			
			db.withdrawas.update({ "_id" : ObjectId(id_withdraw) }, { '$set': {"active_email": 1, "tx": dataSend, "status": 1 } })
	return json.dumps({'status':'Send Success'})