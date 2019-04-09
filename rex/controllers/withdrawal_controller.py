from flask import Blueprint, request, session, redirect, url_for, render_template, flash
from flask.ext.login import login_user, logout_user, current_user, login_required
from rex import app, db
from rex.models import user_model, deposit_model, history_model, invoice_model, wallet_model, withdrawal_model, withdrawal_payment_model
import json
import urllib
import urllib2
from bson.objectid import ObjectId
from block_io import BlockIo
import datetime
from datetime import datetime
from datetime import datetime, date, timedelta
from time import gmtime, strftime
import time
from werkzeug.security import generate_password_hash, check_password_hash
import requests
__author__ = 'carlozamagni'

withdrawal_ctrl = Blueprint('withdrawal', __name__, static_folder='static', template_folder='templates')

def check_password(pw_hash, password):
        return check_password_hash(pw_hash, password)
@withdrawal_ctrl.route('/withdrawal', methods=['GET', 'POST'])
def withdraw():
	if session.get(u'logged_in') is None:
		return redirect('/user/login')
	else:
		uid = session.get('uid')
		user = db.User.find_one({'customer_id': uid})
		withdraw = db.Withdrawal.find({'uid': uid})
		refferal_link = 'http://%s/user/register/%s' % (request.host,uid)
		data_ticker = db.tickers.find_one({})
		data ={
			'refferal_link' : refferal_link,
		    'user': user,
		    'menu' : 'withdrawal',
		    'float' : float,
		    'withdraw' : withdraw,
		    'btc_usd':data_ticker['btc_usd'],
		    'sva_btc':data_ticker['sva_btc'],
		    'sva_usd':data_ticker['sva_usd']
		}
		return render_template('account/withdrawal.html', data=data)
@withdrawal_ctrl.route('/withdraw-submit', methods=['GET', 'POST'])
def Submit():
	if session.get(u'logged_in') is None:
		return redirect('/user/login')
	else:
		uid = session.get('uid')
		user = db.User.find_one({'customer_id': uid})
		if request.method == 'POST' and user.btc_wallet != '':
			if request.form['amount'] =='' and request.form['password'] =='':
				flash({'msg':'Invalid amount. Please try again!', 'type':'danger'})
				flash({'msg':'Invalid Password. Please try again!', 'type':'danger'})
				return redirect('/account/withdrawal')
			if request.form['amount'] =='':
				flash({'msg':'Invalid amount. Please try again!', 'type':'danger'})
				return redirect('/account/withdrawal')
			if request.form['password'] =='':
				flash({'msg':'Invalid Password. Please try again!', 'type':'danger'})
				return redirect('/account/withdrawal')
			amount_current = float(user.s_wallet)/1000000
			amount_form = float(request.form['amount'])
			if amount_form > amount_current and check_password(user.password_transaction, request.form['password']) == False:
				flash({'msg':'Invalid amount. Please try again!', 'type':'danger'})
				flash({'msg':'Invalid password. Please try again!', 'type':'danger'})
				return redirect('/account/withdrawal')

			if amount_form > amount_current or amount_form < 10:
				flash({'msg':'Invalid amount. Please try again!', 'type':'danger'})
				return redirect('/account/withdrawal')
			if check_password(user.password_transaction, request.form['password']) == False:
				flash({'msg':'Invalid password. Please try again!', 'type':'danger'})
				return redirect('/account/withdrawal')
			amount_rest = float(amount_current)-float(amount_form)
			if request.form['method_payment'] =='btc':
				response_btc = urllib2.urlopen("https://blockchain.info/tobtc?currency=USD&value=%s"%(amount_form))
				response_btc = response_btc.read()
				response_btc = json.loads(response_btc)
				response_btc = round(response_btc, 8)
				amount_btc = response_btc*100000000
				method_payment = 0
				wallet_withdraw= user.btc_wallet
				dta_withdraw = {
					'uid':  uid,
					'detail':  'Withdrawal %s $' %(amount_form),
					'amount_sub' :  float(amount_form)*0.97,
					'amount_rest' : float(amount_rest)*1000000,
					'amount_btc' : float(amount_btc)*0.97,
					'txtid':  '',
					'status': 1,
					'date_added' : datetime.utcnow(),
					'wallet' : wallet_withdraw,
					'method_payment': method_payment
				}
				db.users.update({ "customer_id" : uid }, { '$set': { "s_wallet": amount_rest*1000000 } })
				withdraw_id = db.withdrawal.insert(dta_withdraw)
				dta_withdraw_payments = {
					'uid':  uid,
					'detail':  'Withdrawal %s $ fee 3 percent' %(amount_form),
					'amount_sub' :  float(amount_form)*0.97,
					'amount_rest' : float(amount_rest)*1000000,
					'amount_btc' : float(amount_btc)*0.97,
					'txtid':  '',
					'status': 1,
					'date_added' : datetime.utcnow(),
					'wallet' : wallet_withdraw,
					'withdraw_id' : withdraw_id,
					'method_payment': method_payment
				}
				withdraw_id = db.withdrawal_payment.insert(dta_withdraw_payments)
			else:
				url_api = "https://api.cryptonator.com/api/ticker/eth-usd"
				r_eth = requests.get(url_api)
				response_eth = r_eth.json()
				price_eth = response_eth['ticker']['price'];
				price_eth = float(price_eth)*100000000
				wallet_withdraw= user.wallet
				method_payment = 1
				amount_btc = float(amount_form)*100000000
				amount = amount_btc/int(price_eth)
				amount = round(amount, 8)
				amount = amount*100000000
				dta_withdraw = {
					'uid':  uid,
					'detail':  'Withdrawal %s $' %(amount_form),
					'amount_sub' :  float(amount_form)*0.97,
					'amount_rest' : float(amount_rest)*1000000,
					'amount_btc' : float(amount)*0.97,
					'txtid':  '',
					'status': 1,
					'date_added' : datetime.utcnow(),
					'wallet' : wallet_withdraw,
					'method_payment': method_payment
				}
				db.users.update({ "customer_id" : uid }, { '$set': { "s_wallet": amount_rest*1000000 } })
				withdraw_id = db.withdrawal.insert(dta_withdraw)
				dta_withdraw_payments = {
					'uid':  uid,
					'detail':  'Withdrawal %s $ fee 3 percent' %(amount_form),
					'amount_sub' :  float(amount_form)*0.97,
					'amount_rest' : float(amount_rest)*1000000,
					'amount_btc' : float(amount)*0.97,
					'txtid':  '',
					'status': 1,
					'date_added' : datetime.utcnow(),
					'wallet' : wallet_withdraw,
					'withdraw_id' : withdraw_id,
					'method_payment': method_payment
				}
				withdraw_id = db.withdrawal_payment.insert(dta_withdraw_payments)

			flash({'msg':'Ordered to withdraw successfully, your transaction will be processed in 24 hours', 'type':'success'})
			return redirect('/account/withdrawal')
	return redirect('/account/withdrawal')

