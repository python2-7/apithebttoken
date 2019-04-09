from flask import Blueprint, request, session, redirect, url_for, render_template, flash
from flask.ext.login import login_user, logout_user, current_user, login_required
from rex import app, db
from rex.models import user_model, deposit_model, history_model, invoice_model
from bson.objectid import ObjectId
from random import randint
import json
import time
import datetime
from datetime import datetime
from datetime import datetime, date, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import onetimepass
import base64
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from urllib2 import urlopen
def check_password(pw_hash, password):
	return check_password_hash(pw_hash, password)
__author__ = 'carlozamagni'

ico_ctrl = Blueprint('ico', __name__, static_folder='static', template_folder='templates')
def finduser_by_id(ids):
	user = db.User.find_one({'_id': ObjectId(ids)})
	return user


def verify_totp(token, otp_secret):
    return onetimepass.valid_totp(token, otp_secret)

@ico_ctrl.route('/mail', methods=['GET', 'POST'])
def sdfasdf():
	username = 'support@smartfva.co'
	password = 'YK45OVfobZ5X'
	msg = MIMEMultipart('mixed')

	sender = 'support@smartfva.co'
	recipient = 'belindatbeach@gmail.com'

	msg['Subject'] = 'Your Subject'
	msg['From'] = sender
	msg['To'] = recipient

	text_message = MIMEText('It is a text message.', 'plain')
	html_message = MIMEText('It is a html message.', 'html')
	msg.attach(text_message)
	msg.attach(html_message)

	mailServer = smtplib.SMTP('mail.smtp2go.com', 2525) # 8025, 587 and 25 can also be used. 
	mailServer.ehlo()
	mailServer.starttls()
	mailServer.ehlo()
	mailServer.login(username, password)
	mailServer.sendmail(sender, recipient, msg.as_string())
	mailServer.close()

	return json.dumps({'adafa':'qwer'})

@ico_ctrl.route('/ico', methods=['GET', 'POST'])
def icoCtrl():
	if session.get(u'logged_in') is None:
		return redirect('/user/login')
	else:
		uid = session.get('uid')
		user = db.User.find_one({'customer_id': uid})
		total_refferal = db.users.find({'p_node': uid}).count()
		username = user['username']
		refferal_link = 'https://smartfva.co/user/register/%s' % (username)
		received = float(user.m_wallet/1000000)
		roi = float(user.roi)
		# query = db.icos.find({}).sort([( 'date_added': -1 )]).limit(10)
		query = db.icos.find().sort([("date_added", -1)]).limit(10)
		if roi > 0:
			percent = received/roi
		else:
			percent = 0		
		data_ticker = db.tickers.find_one({})
		max_out = float(user.max_out)
		total_max_out = int(user.total_max_out)
		if max_out > 0:
			percent_max = total_max_out/max_out
		else:
			percent_max = 0
		data ={
			'refferal_link' : refferal_link,
		    'user': user,
		    'ico' : query,
		    'menu' : 'ico',
		    'float' : float,
		    'percent' : round(percent*100, 2),
		    'percent_max' : round(percent_max*100, 2),
		    'referer': int(total_refferal),
		    'btc_usd':data_ticker['btc_usd'],
	        'sva_btc':data_ticker['sva_btc'],
	        'sva_usd':data_ticker['sva_usd']
		}
		
		return render_template('account/ico.html', data=data)
@ico_ctrl.route('/checkUsername', methods=['GET', 'POST'])
def checkUsername():
	if session.get(u'logged_in') is None:
		return json.dumps({
			'status': 'error', 
			'message': 'Please Login' 
		})
	else:
		if request.method == 'POST':
			user_id = session.get('user_id')
			uid = session.get('uid')
			myuser = db.users.find_one({'_id': ObjectId(user_id)})
			username = request.form['username']
			if request.form['username'] == '':
				return json.dumps({
					'status': 'error', 
					'message': 'Please enter Recipient Username' 
				})
			username = username.lower()
			user = db.User.find_one({'$and': [{'username': username}, {'username' :{'$ne': myuser['username']}}]} )
			if user:
				return json.dumps({
					'status': 'success', 
					'message': 'username exists' 
				})
			else:
				return json.dumps({
					'status': 'error', 
					'message': 'Username does not exist' 
				})
		else:
			return json.dumps({
				'status': 'error', 
				'message': '' 
			})
def is_number(s):
    try:
        complex(s) # for int, long, float and complex
    except ValueError:
        return False
    return True
@ico_ctrl.route('/transferAccount', methods=['GET', 'POST'])
def transferAccount():
	return json.dumps({ 'status': 'error', 'message': 'Coming Soon' })
	if session.get(u'logged_in') is None:
		return json.dumps({
			'status': 'error', 
			'message': 'Please Login' 
		})
	else:
		if request.method == 'POST':
			user_id = session.get('user_id')
			uid = session.get('uid')
			myuser = db.users.find_one({'_id': ObjectId(user_id)})
			# if uid != '11201729184754' or myuser['code_active'] != 'P913L1':
			# 	return json.dumps({
			# 		'status': 'error', 
			# 		'message': 'Coming Soon!' 
			# 	})
			# if myuser['username'] != 'success':
			# 	return json.dumps({
			# 		'status': 'error', 
			# 		'message': 'Coming Soon' 
			# 	})
			username = request.form['username']
			sva_amount = request.form['sva_amount']
			password = request.form['password']
			if username == '':
				return json.dumps({
					'status': 'error', 
					'message': 'Please enter Recipient Username' 
				})
			checkIsNumberSVA = is_number(sva_amount)
			sva_balance = myuser['sva_balance']

			if sva_amount == '' or checkIsNumberSVA == False or float(sva_amount) < 5 or float(sva_balance) < float(sva_amount):
				return json.dumps({
					'status': 'error', 
					'message': 'Please enter valid quantity (quantity > 5)' 
				})
			if check_password(myuser['password'], password) == False:
				return json.dumps({
					'status': 'error', 
					'message': 'Wrong password' 
				})
			if myuser['status_2fa'] == 1:
				onetime = request.form['one_time_password']
				checkVerifY = verify_totp(onetime, myuser['secret_2fa'])
				if checkVerifY == False:
					msg = 'The two-factor authentication code you specified is incorrect. Please check the clock on your authenticator device to verify that it is in sync'
					return json.dumps({
						'status': 'error', 
						'message': msg
					})
			username = username.lower()
			userReceive = db.User.find_one({'$and': [{'username': username}, {'username' :{'$ne': myuser['username']}}]} )
			if userReceive:
				sva_amount = float(sva_amount)
				sva_amount =round(sva_amount,8)
				sva_balance_receive = userReceive['sva_balance']
				new_sva_balance = float(sva_balance) - float(sva_amount)
				new_sva_balance = round(new_sva_balance, 8)
				db.users.update({ "_id" : ObjectId(user_id) }, { '$set': { "sva_balance": float(new_sva_balance) } })
				data_history = {
					'uid' : uid,
					'user_id': user_id,
					'username' : myuser['username'],
					'amount': float(sva_amount),
					'type' : 'send',
					'wallet': 'SVA',
					'date_added' : datetime.utcnow(),
					'detail': 'Transfer %s SVA from SVA Wallet to account %s' %(float(sva_amount), userReceive['username']),
					'rate': '',
					'txtid' : '' ,
					'amount_sub' : 0,
					'amount_add' : 0,
					'amount_rest' : 0
				}
				db.historys.insert(data_history)
				new_sva_balance_receive = float(sva_balance_receive)+float(sva_amount)
				new_sva_balance_receive = round(new_sva_balance_receive, 8)
				db.users.update({ "_id" : ObjectId(userReceive['_id']) }, { '$set': { "sva_balance": float(new_sva_balance_receive) } })
				data_history = {
					'uid' : userReceive['customer_id'],
					'user_id': userReceive['_id'],
					'username' : userReceive['username'],
					'amount': float(sva_amount),
					'type' : 'receive',
					'wallet': 'SVA',
					'date_added' : datetime.utcnow(),
					'detail': 'Receive %s SVA from account %s' %(float(sva_amount), myuser['username']),
					'rate': '',
					'txtid' : '' ,
					'amount_sub' : 0,
					'amount_add' : 0,
					'amount_rest' : 0
				}
				db.historys.insert(data_history)

				return json.dumps({
					'status': 'success', 
					'message': 'Transfer to %s Success' %(username),
					'new_sva_balance': new_sva_balance
				})
			else:
				return json.dumps({
					'status': 'error', 
					'message': 'Please enter Recipient Username' 
				})
		else:
			return json.dumps({
				'status': 'error', 
				'message': '' 
			})

def SaveHistory(uid, user_id, username, amount, types, wallet, detail, rate, txtid):
    data_history = {
        'uid' : uid,
        'user_id': user_id,
        'username' : username,
        'amount': float(amount),
        'type' : types,
        'wallet': wallet,
        'date_added' : datetime.utcnow(),
        'detail': detail,
        'rate': rate,
        'txtid' : txtid,
        'amount_sub' : 0,
        'amount_add' : 0,
        'amount_rest' : 0
    }
    db.historys.insert(data_history)
    return True
def FnRefferalProgram(user_id, amount_invest):
    customer = db.users.find_one({"customer_id" : user_id })
    username_invest = customer['username']
    if customer['p_node'] != '0' or customer['p_node'] != '':
        for x in xrange(1,4):
            customer_p_node = db.users.find_one({"customer_id" : customer['p_node'] })
            if customer_p_node:
                if x == 1:
                    commission = float(amount_invest)*0.08
                    commission = round(commission,2)
                    sva_balance = float(customer_p_node['sva_balance'])
                    new_sva_balance = float(commission) + float(sva_balance)
                    db.users.update({ "_id" : ObjectId(customer_p_node['_id']) }, { '$set': { "sva_balance": new_sva_balance } })
                    detail = 'Get 8 '+"""%"""+' referral bonus from member %s buy %s SVA' %(username_invest, amount_invest)
                    SaveHistory(customer_p_node['customer_id'],customer_p_node['_id'],customer_p_node['username'], commission, 'receive', 'SVA', detail, '', '')
                if x == 2:
                    commission = float(amount_invest)*0.02
                    commission = round(commission,2)
                    sva_balance = float(customer_p_node['sva_balance'])
                    new_sva_balance = float(commission) + float(sva_balance)
                    db.users.update({ "_id" : ObjectId(customer_p_node['_id']) }, { '$set': { "sva_balance": new_sva_balance } })
                    detail = 'Get 2 '+"""%"""+' referral bonus from member %s buy %s SVA' %(username_invest, amount_invest)
                    SaveHistory(customer_p_node['customer_id'],customer_p_node['_id'],customer_p_node['username'], commission, 'receive', 'SVA', detail, '', '')
                if x == 3:
                    commission = float(amount_invest)*0.01
                    commission = round(commission,2)
                    sva_balance = float(customer_p_node['sva_balance'])
                    new_sva_balance = float(commission) + float(sva_balance)
                    db.users.update({ "_id" : ObjectId(customer_p_node['_id']) }, { '$set': { "sva_balance": new_sva_balance } })
                    detail = 'Get 1 '+"""%"""+' referral bonus from member %s buy %s SVA' %(username_invest, amount_invest)
                    SaveHistory(customer_p_node['customer_id'],customer_p_node['_id'],customer_p_node['username'], commission, 'receive', 'SVA', detail, '', '')
            else:
            	return True
            if customer_p_node['customer_id'] == '1010101001' or customer_p_node['p_node'] == '0' or customer_p_node['p_node'] == '':
                return True
            else:
            	customer = db.users.find_one({"customer_id" : customer_p_node['customer_id'] })
    return True

@ico_ctrl.route('/buyIco', methods=['GET', 'POST'])
def buyIco():
	if session.get(u'logged_in') is None:
		return json.dumps({
			'status': 'error', 
			'message': 'Please Login' 
		})
	else:
		if request.method == 'POST':
			user_id = session.get('user_id')
			uid = session.get('uid')
			myuser = db.users.find_one({'_id': ObjectId(user_id)})
			sva_amount = request.form['sva_amount']
			btc_amount = request.form['btc_amount']
			password = request.form['password']

			ico_sum = db.icosums.find_one({})
			if float(ico_sum['total_today']) >= 150000 and myuser['username'] != 'smartfvasmartfva':
				return json.dumps({
					'status': 'error', 
					'message': 'Sold out' 
				})
			checkIsNumberSVA = is_number(sva_amount)
			checkIsNumberBTC = is_number(btc_amount)
			if sva_amount == '' or checkIsNumberSVA == False or checkIsNumberBTC == False or float(sva_amount) < 50 or float(sva_amount) > 50000:
				return json.dumps({
					'status': 'error', 
					'message': 'Please enter valid quantity (quantity > 50)' 
				})
			sva_amount = float(sva_amount)
			# sva_amount = round(sva_amount, 0)
			if check_password(myuser['password'], password) == False:
				return json.dumps({
					'status': 'error', 
					'message': 'Wrong password' 
				})
			if myuser['status_2fa'] == 0:
				return json.dumps({
					'status': 'error', 
					'message': 'Please setup your Two Factor Auth'
				})
			onetime = request.form['one_time_password']
			print onetime
			print myuser['secret_2fa']
			checkVerifY = verify_totp(onetime, myuser['secret_2fa'])
			if checkVerifY == False:
				msg = 'The two-factor authentication code you specified is incorrect. Please check the clock on your authenticator device to verify that it is in sync'
				return json.dumps({
					'status': 'error', 
					'message': msg
				})

			btc_balance = myuser['btc_balance']
			data_ticker = db.tickers.find_one({})
			btc_usd = data_ticker['btc_usd']
			sva_usd = data_ticker['sva_usd']
			convert_sva_amount_usd = float(sva_amount)*float(sva_usd)
			convert_sva_amount_usd = round(convert_sva_amount_usd,2)

			sva_btc = convert_sva_amount_usd/float(btc_usd)

			sva_btc = round(sva_btc, 8)
			satoshi_btc_balance = float(btc_balance)*100000000
			sva_btc_satoshi_form = float(btc_amount)*100000000
			satoshi_sva_btc = float(sva_btc)*100000000
			if sva_btc_satoshi_form >=  satoshi_sva_btc:
				satoshi_sva_btc = sva_btc_satoshi_form
			if satoshi_sva_btc > satoshi_btc_balance:
				return json.dumps({
					'status': 'error', 
					'message': 'Your balance is not enough' 
				})

			url_api = 'http://192.254.72.34:38058/rabbitico?userid='+str(user_id)+'&amount='+str(sva_amount)
			r = requests.get(url_api)
			time.sleep(1)
			return json.dumps({
				'status': 'success', 
				'message': '' 
			})
		else:
			return json.dumps({
				'status': 'error', 
				'message': '' 
			})

@ico_ctrl.route('/buyIco_bk', methods=['GET', 'POST'])
def buyIco_bk():
	if session.get(u'logged_in') is None:
		return json.dumps({
			'status': 'error', 
			'message': 'Please Login' 
		})
	else:
		if request.method == 'POST':
			# if randint(0, 1) == 0:
			# 	return json.dumps({
			# 	'status': 'error', 
			# 	'message': 'Error network! Please try again' 
			# 	})
			user_id = session.get('user_id')
			uid = session.get('uid')
			myuser = db.users.find_one({'_id': ObjectId(user_id)})
			sva_amount = request.form['sva_amount']
			btc_amount = request.form['btc_amount']
			password = request.form['password']

			ico_sum = db.icosums.find_one({})
			if float(ico_sum['total_today']) >= 150000:
				return json.dumps({
					'status': 'error', 
					'message': 'Sold out' 
				})

			checkIsNumberSVA = is_number(sva_amount)
			checkIsNumberBTC = is_number(btc_amount)
			if sva_amount == '' or checkIsNumberSVA == False or checkIsNumberBTC == False or float(sva_amount) < 50 or float(sva_amount) > 500:
				return json.dumps({
					'status': 'error', 
					'message': 'Please enter valid quantity (quantity > 50 and < 500)' 
				})
			sva_amount = float(sva_amount)
			# sva_amount = round(sva_amount, 0)
			if check_password(myuser['password'], password) == False:
				return json.dumps({
					'status': 'error', 
					'message': 'Wrong password' 
				})
			if myuser['status_2fa'] == 0:
				return json.dumps({
					'status': 'error', 
					'message': 'Please setup your Two Factor Auth'
				})
			onetime = request.form['one_time_password']
			print onetime
			print myuser['secret_2fa']
			checkVerifY = verify_totp(onetime, myuser['secret_2fa'])
			if checkVerifY == False:
				msg = 'The two-factor authentication code you specified is incorrect. Please check the clock on your authenticator device to verify that it is in sync'
				return json.dumps({
					'status': 'error', 
					'message': msg
				})
			btc_balance = myuser['btc_balance']
			data_ticker = db.tickers.find_one({})
			btc_usd = data_ticker['btc_usd']
			sva_usd = data_ticker['sva_usd']
			convert_sva_amount_usd = float(sva_amount)*float(sva_usd)
			convert_sva_amount_usd = round(convert_sva_amount_usd,2)

			sva_btc = convert_sva_amount_usd/float(btc_usd)

			sva_btc = round(sva_btc, 8)
			satoshi_btc_balance = float(btc_balance)*100000000
			sva_btc_satoshi_form = float(btc_amount)*100000000
			satoshi_sva_btc = float(sva_btc)*100000000
			if sva_btc_satoshi_form >=  satoshi_sva_btc:
				satoshi_sva_btc = sva_btc_satoshi_form
			if satoshi_sva_btc > satoshi_btc_balance:
				return json.dumps({
					'status': 'error', 
					'message': 'Your balance is not enough' 
				})
			new_btc_balance_satoshi=float(satoshi_btc_balance) - float(satoshi_sva_btc)
			new_btc_balance = float(new_btc_balance_satoshi)/100000000
			new_btc_balance = round(new_btc_balance, 8)
			sva_balance = myuser['sva_balance']
			new_sva_balance = float(sva_amount)+float(sva_balance)
			new_sva_balance = round(new_sva_balance, 8)

			ico_total_today = ico_sum['total_today']
			new_ico_total_today = float(ico_total_today)+float(sva_amount)
			ico_total = ico_sum['total']
			new_ico_total = float(ico_total)+float(sva_amount)
			new_ico_total=round(new_ico_total,0)

			check_total_today = is_number(new_ico_total_today)
			check_total = is_number(new_ico_total)

			if check_total_today == False or check_total == False:
				return json.dumps({
					'status': 'error', 
					'message': 'Error network! Please try again' 
				})
			db.icosums.update({}, { '$set': { "total": new_ico_total } })

			check_new_btc_balance = is_number(new_btc_balance)
			check_new_sva_balance = is_number(new_sva_balance)
			if check_new_btc_balance == False or check_new_sva_balance == False:
				return json.dumps({
					'status': 'error', 
					'message': 'Error network! Please try again' 
				})
			FnRefferalProgram(uid, sva_amount)
			db.users.update({ "_id" : ObjectId(user_id) }, { '$set': {"m_wallet": 1, "btc_balance": new_btc_balance, 'sva_balance': float(new_sva_balance) } })
			data_history = {
				'uid' : uid,
				'user_id': user_id,
				'username' : myuser['username'],
				'amount': float(sva_btc),
				'type' : 'send',
				'wallet': 'BTC',
				'date_added' : datetime.utcnow(),
				'detail': 'Send %s BTC to buy %s SVA' %(sva_btc, sva_amount),
				'rate': '1 SVA = %s USD' %(sva_usd),
				'txtid' : '' ,
				'amount_sub' : 0,
				'amount_add' : 0,
				'amount_rest' : 0
			}
			db.historys.insert(data_history)

			data_order = {
				'uid' : uid,
				'user_id': user_id,
				'username' : myuser['username'],
				'amount_sva': float(sva_amount),
				'amount_btc': float(sva_btc),
				'date_added' : datetime.utcnow(),
				
				'rate': float(sva_usd)
			}
			db.icos.insert(data_order)

			data_history_sva = {
				'uid' : uid,
				'user_id': user_id,
				'username' : myuser['username'],
				'amount': float(sva_amount),
				'type' : 'receive',
				'wallet': 'SVA',
				'date_added' : datetime.utcnow(),
				'detail': 'Buy %s SVA' %(float(sva_amount)),
				'rate': '1 SVA = %s USD' %(sva_usd),
				'txtid' : '' ,
				'amount_sub' : 0,
				'amount_add' : 0,
				'amount_rest' : 0
			}
			db.historys.insert(data_history_sva)

			return json.dumps({
				'status': 'success', 
				'message': 'Buy SVA Success',
				'new_sva_balance': new_sva_balance,
				'new_btc_balance': new_btc_balance
			})
		else:
			return json.dumps({
				'status': 'error', 
				'message': '' 
			})
@ico_ctrl.route('/exchangeToken', methods=['GET', 'POST'])
def exchangeToken():
	if session.get(u'logged_in') is None:
		return json.dumps({
			'status': 'error', 
			'message': 'Please Login' 
		})
	else:
		if request.method == 'POST':
			if request.form['amount_token'] == '':
				return json.dumps({
					'status': 'error', 
					'message': 'Please enter amount exchange!' 
				})
			amount = float(request.form['amount_token'])
			amount = round(amount, 2)
			if float(amount) < 10:
				return json.dumps({
					'status': 'error', 
					'message': 'Please enter amount is number and value greater than 10' 
				})

			user_id = session.get('user_id')
			uid = session.get('uid')
			user = db.users.find_one({'_id': ObjectId(user_id)})
			token_balance = user['s_token']
			sva_balance = user['sva_balance']		
			new_usd_sva = float(amount)/10
			new_usd_sva = round(new_usd_sva, 8)
			if float(token_balance) < float(amount):
				return json.dumps({
					'status': 'error', 
					'message': 'Your balance is not enough!' 
				})
			new_token_balance = float(token_balance) - float(amount)
			new_token_balance = round(new_token_balance, 2)
			new_sva_balance = float(sva_balance) + float(new_usd_sva)
			new_sva_balance = round(new_sva_balance, 8)
			db.users.update({ "_id" : ObjectId(user_id) }, { '$set': { "s_token": new_token_balance, "sva_balance": new_sva_balance } })
			data_history = {
				'uid' : uid,
				'user_id': user_id,
				'username' : user['username'],
				'amount': float(new_usd_sva),
				'type' : 'receive',
				'wallet': 'SVA',
				'date_added' : datetime.utcnow(),
				'detail': 'Receive %s SVA from Token Wallet (%s Token)' %(new_usd_sva, amount),
				'rate': '1 SVA = 10 Token',
				'txtid' : '' ,
				'amount_sub' : 0,
				'amount_add' : 0,
				'amount_rest' : 0
			}
			db.historys.insert(data_history)
			return json.dumps({
				'status': 'success',
				'new_token': new_token_balance,
				'new_sva_balance': new_sva_balance,
				'message': 'Transfer to SVA Wallet success!'
			})
		else:
			return json.dumps({
				'status': 'error', 
				'message': '403 Forbidden' 
			})

@ico_ctrl.route('/buyIcobuyIco', methods=['GET', 'POST'])
def buyIcobuyIco():
	if session.get(u'logged_in') is None:
		return json.dumps({
			'status': 'error', 
			'message': 'Please Login' 
		})
	else:

		if request.method == 'GET':
			user_id = session.get('user_id')
			uid = session.get('uid')
			myuser = db.users.find_one({'_id': ObjectId(user_id)})
			sva_amount = 100
			btc_amount = 0.0023441
			password = '12345'
			ico_sum = db.icosums.find_one({})
			if float(ico_sum['total_today']) >= 50000:
				return json.dumps({
					'status': 'error', 
					'message': 'Sold out' 
				})
			checkIsNumberSVA = is_number(sva_amount)
			checkIsNumberBTC = is_number(btc_amount)
			if sva_amount == '' or checkIsNumberSVA == False or checkIsNumberBTC == False or float(sva_amount) < 50 or float(sva_amount) > 50000:
				return json.dumps({
					'status': 'error', 
					'message': 'Please enter valid quantity (quantity > 50 and < 5000)' 
				})
			sva_amount = float(sva_amount)
			# sva_amount = round(sva_amount, 0)
			if check_password(myuser['password'], password) == False:
				return json.dumps({
					'status': 'error', 
					'message': 'Wrong password' 
				})
			# if myuser['status_2fa'] == 1:
			onetime = request.form['one_time_password']
			print onetime
			checkVerifY = verify_totp(onetime, myuser['secret_2fa'])
			if checkVerifY == False:
				msg = 'The two-factor authentication code you specified is incorrect. Please check the clock on your authenticator device to verify that it is in sync'
				return json.dumps({
					'status': 'error', 
					'message': msg
				})
			btc_balance = myuser['btc_balance']
			data_ticker = db.tickers.find_one({})
			btc_usd = data_ticker['btc_usd']
			sva_usd = data_ticker['sva_usd']
			convert_sva_amount_usd = float(sva_amount)*float(sva_usd)
			convert_sva_amount_usd = round(convert_sva_amount_usd,2)

			sva_btc = convert_sva_amount_usd/float(btc_usd)

			sva_btc = round(sva_btc, 8)
			satoshi_btc_balance = float(btc_balance)*100000000
			sva_btc_satoshi_form = float(btc_amount)*100000000
			satoshi_sva_btc = float(sva_btc)*100000000
			if sva_btc_satoshi_form >=  satoshi_sva_btc:
				satoshi_sva_btc = sva_btc_satoshi_form
			if satoshi_sva_btc > satoshi_btc_balance:
				return json.dumps({
					'status': 'error', 
					'message': 'Your balance is not enough' 
				})
			new_btc_balance_satoshi=float(satoshi_btc_balance) - float(satoshi_sva_btc)
			new_btc_balance = float(new_btc_balance_satoshi)/100000000
			new_btc_balance = round(new_btc_balance, 8)
			sva_balance = myuser['sva_balance']
			new_sva_balance = float(sva_amount)+float(sva_balance)
			new_sva_balance = round(new_sva_balance, 8)

			ico_total_today = ico_sum['total_today']
			new_ico_total_today = float(ico_total_today)+float(sva_amount)
			ico_total = ico_sum['total']
			new_ico_total = float(ico_total)+float(sva_amount)
			new_ico_total=round(new_ico_total,0)

			check_total_today = is_number(new_ico_total_today)
			check_total = is_number(new_ico_total)

			if check_total_today == False or check_total == False:
				return json.dumps({
					'status': 'error', 
					'message': 'Error network!' 
				})
			db.icosums.update({}, { '$set': { "total": new_ico_total, 'total_today': float(new_ico_total_today) } })

			check_new_btc_balance = is_number(new_btc_balance)
			check_new_sva_balance = is_number(new_sva_balance)
			if check_new_btc_balance == False or check_new_sva_balance == False:
				return json.dumps({
					'status': 'error', 
					'message': 'Error network!' 
				})
			FnRefferalProgram(uid, sva_amount)
			db.users.update({ "_id" : ObjectId(user_id) }, { '$set': {"m_wallet": 1, "btc_balance": new_btc_balance, 'sva_balance': float(new_sva_balance) } })
			data_history = {
				'uid' : uid,
				'user_id': user_id,
				'username' : myuser['username'],
				'amount': float(sva_btc),
				'type' : 'send',
				'wallet': 'BTC',
				'date_added' : datetime.utcnow(),
				'detail': 'Send %s BTC to buy %s SVA' %(sva_btc, sva_amount),
				'rate': '1 SVA = %s USD' %(sva_usd),
				'txtid' : '' ,
				'amount_sub' : 0,
				'amount_add' : 0,
				'amount_rest' : 0
			}
			db.historys.insert(data_history)

			data_order = {
				'uid' : uid,
				'user_id': user_id,
				'username' : myuser['username'],
				'amount_sva': float(sva_amount),
				'amount_btc': float(sva_btc),
				'date_added' : datetime.utcnow(),
				
				'rate': float(sva_usd)
			}
			db.icos.insert(data_order)

			data_history_sva = {
				'uid' : uid,
				'user_id': user_id,
				'username' : myuser['username'],
				'amount': float(sva_amount),
				'type' : 'receive',
				'wallet': 'SVA',
				'date_added' : datetime.utcnow(),
				'detail': 'Buy %s SVA' %(float(sva_amount)),
				'rate': '1 SVA = %s USD' %(sva_usd),
				'txtid' : '' ,
				'amount_sub' : 0,
				'amount_add' : 0,
				'amount_rest' : 0
			}
			db.historys.insert(data_history_sva)

			return json.dumps({
				'status': 'success', 
				'message': 'Buy SVA Success',
				'new_sva_balance': new_sva_balance,
				'new_btc_balance': new_btc_balance
			})
		else:
			return json.dumps({
				'status': 'error', 
				'message': '' 
			})			