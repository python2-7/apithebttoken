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

from rex.config import Config
withdrawal_ctrl = Blueprint('withdraw', __name__, static_folder='static', template_folder='templates')


@withdrawal_ctrl.route('/withdraw-confirm/<code>', methods=['GET', 'POST'])
def withdraw_currency_confirm(code):
	
	withdraw = db.withdraws.find_one({'$and' : [{'code_active' : code},{'active_email' : 0}]})

	if withdraw is not None:
		db.withdraws.update({'_id' : ObjectId(withdraw['_id'])},{'$set' : {'active_email' : 1}})
		amount = withdraw['amount']
		customer_id = withdraw['uid']
		price_atlcoin = withdraw['price']
		address = withdraw['address']
		currency = withdraw['currency']
		
		user = db.User.find_one({'customer_id': customer_id})
		if user is not None:
			if currency == 'BTC':
				val_balance = user['balance']['bitcoin']['available']
				string_query = 'balance.bitcoin.available'
				min_withdraw = 0.002
			if currency == 'ETH':
				val_balance = user['balance']['ethereum']['available']
				string_query = 'balance.ethereum.available'
				min_withdraw = 0.02
			if currency == 'LTC':
				val_balance = user['balance']['litecoin']['available']
				string_query = 'balance.litecoin.available'
				min_withdraw = 0.002
			if currency == 'XRP':
				val_balance = user['balance']['ripple']['available']
				string_query = 'balance.ripple.available'
				min_withdraw = 22
			if currency == 'USDT':
				val_balance = user['balance']['tether']['available']
				string_query = 'balance.tether.available'
				min_withdraw = 6.6
			if currency == 'DASH':
				val_balance = user['balance']['dash']['available']
				string_query = 'balance.dash.available'
				min_withdraw = 0.004
			if currency == 'EOS':
				val_balance = user['balance']['eos']['available']
				string_query = 'balance.eos.available'
				min_withdraw = 0.2
			if currency == 'BCH':
				val_balance = user['balance']['bch']['available']
				string_query = 'balance.bch.available'
				min_withdraw = 0.2
			if currency == 'TBT':
				val_balance = user['balance']['coin']['available']
				string_query = 'balance.coin.available'
				min_withdraw = 0.1


	        if float(val_balance) >= (float(amount)*100000000):
	        	if float(user['balance']['coin']['available']) >= 100000:
					amount_usd = float(amount)*float(price_atlcoin)
                      
					new_balance_sub = round(float(val_balance) - (float(amount)*100000000),8)

					db.users.update({ "customer_id" : customer_id }, { '$set': { string_query: float(new_balance_sub) } })

					#save lich su
					data = {
					  'user_id': user['_id'],
					  'uid': user['customer_id'],
					  'username': user['username'],
					  'amount': float(amount),
					  'type': 'withdraw',
					  'txt_id': 'Pending',
					  'date_added' : datetime.utcnow(),
					  'status': 0,
					  'address': address,
					  'currency' : currency,
					  'confirmations' : 0,
					  'amount_usd': float(price_atlcoin) * float(amount),
					  'price' : price_atlcoin,
					  'id_coinpayment' : ''
					}
					db.wallets.insert(data)
					#fee
					userss = db.User.find_one({'customer_id': customer_id})
					new_coin_fee = round((float(userss['balance']['coin']['available']) - 100000),8)
					db.users.update({ "customer_id" : customer_id }, { '$set': { 'balance.coin.available' : new_coin_fee } })

					
					send_mail_withdraw_admin(user['email'],amount,currency,address)
					return redirect('https://thebesttoken.co#withdraw-success')
	
	return redirect('https://thebesttoken.co#withdraw-error')


def send_mail_withdraw_admin(email,amount,currency,address):
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