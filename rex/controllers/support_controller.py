from flask import Blueprint, request, session, redirect, url_for, render_template, flash
from flask.ext.login import login_user, logout_user, current_user, login_required
from rex import app, db
from rex.models import user_model, deposit_model, history_model, invoice_model
import urllib
import urllib2
import json
from bson.objectid import ObjectId
from datetime import datetime
__author__ = 'carlozamagni'

support_ctrl = Blueprint('support', __name__, static_folder='static', template_folder='templates')


@support_ctrl.route('/support', methods=['GET', 'POST'])
def support():
	#return redirect('/account/login')
	if session.get(u'logged_in') is None:
		return redirect('/user/login')
	uid = session.get('uid')
	user_id = session.get('user_id')
	query = db.supports.find({'user_id': user_id})
	user = db.User.find_one({'customer_id': uid})
	list_notifications = db.notifications.find({'$and' : [{'read' : 0},{'status' : 0},{'$or' : [{'uid' : uid},{'type' : 'all'}]}]})
	number_notifications = list_notifications.count()
	data ={
	'support' : query,
	'title': 'Support',
	'menu' : 'support',
	'user': user,
	'uid': uid,
	'number_notifications' : number_notifications,
    'list_notifications' : list_notifications,
	}
	return render_template('account/support.html', data=data)

@support_ctrl.route('/new-support', methods=['GET', 'POST'])
def newsupports():
	if session.get(u'logged_in') is None:
		return redirect('/user/login')
	uid = session.get('uid')
	user_id = session.get('user_id')
	query = db.supports.find({'user_id': user_id})
	user = db.User.find_one({'customer_id': uid})
	list_notifications = db.notifications.find({'$and' : [{'read' : 0},{'status' : 0},{'$or' : [{'uid' : uid},{'type' : 'all'}]}]})
	number_notifications = list_notifications.count()
	data ={
		'support' : query,
		'title': 'Support',
		'menu' : 'support',
		'user': user,
		'uid': uid,
		'number_notifications' : number_notifications,
	    'list_notifications' : list_notifications,
	}
	return render_template('account/new-support.html', data=data)

@support_ctrl.route('/support/<ids>', methods=['GET', 'POST'])
def Replysupport(ids):
	if session.get(u'logged_in') is None:
		return redirect('/user/login')
	uid = session.get('uid')
	user_id = session.get('user_id')
	support = db.supports.find_one({'_id': ObjectId(ids)})
	user = db.User.find_one({'customer_id': uid})
	data_ticker = db.tickers.find_one({})
	list_notifications = db.notifications.find({'$and' : [{'read' : 0},{'status' : 0},{'$or' : [{'uid' : uid},{'type' : 'all'}]}]})
	number_notifications = list_notifications.count()
	data ={
	'data_support' : support,
	'title': 'Support',
	'menu' : 'support',
	'user': user,
	'uid': uid,
	'number_notifications' : number_notifications,
    'list_notifications' : list_notifications,
	}
	return render_template('account/reply_support.html', data=data)

@support_ctrl.route('/support/reply-support', methods=['POST'])
def newsupporReplyt():
	if session.get(u'logged_in') is None:
		flash({'msg':'Please login', 'type':'danger'})
		return redirect('/user/login')
	if request.method == 'POST':
		user_id = session.get('user_id')
		sp_id = request.form['sp_id']
		support = db.supports.find_one({'_id': ObjectId(sp_id)})
		if support is None:
			flash({'msg':'Not Found', 'type':'danger'})
			return redirect('/account/support/'+str(sp_id))
		else: 
			user = db.users.find_one({'_id': ObjectId(user_id)})
			message = request.form['message']
			recaptcha = request.form['g-recaptcha-response']
	        if  message == '':
	            flash({'msg':'Please enter message', 'type':'danger'})
	            return redirect('/account/support/'+str(sp_id))
	        if recaptcha == '':
	            flash({'msg':'Please check captcha', 'type':'danger'})
	            return redirect('/account/support/'+str(sp_id))
	        else:        
				api_url = 'https://www.google.com/recaptcha/api/siteverify'
				site_key = '6LcESjUUAAAAAN0l4GsSiE2cLLZLZQSRZsEdSroE'
				secret_key = '6LcESjUUAAAAAGsX2iLiwlnbBUyUsZXTz7jrPfAX'
				site_key_post = recaptcha
				ret = urllib2.urlopen('https://api.ipify.org')
				remoteip = ret.read()
				api_url = str(api_url)+'?secret='+str(secret_key)+'&response='+str(site_key_post)+'&remoteip='+str(remoteip);
				response = urllib2.urlopen(api_url)
				response = response.read()
				response = json.loads(response)
				print(response)
				if response['success']:
					data_support = {
					'user_id': user_id,
					'username' : user['username'],
					'message': message,
					'date_added' : datetime.utcnow()
					}
					db.supports.update({ "_id" : ObjectId(sp_id) }, { '$set': { "status": 0 }, '$push':{'reply':data_support } })
					#flash({'msg':'Success', 'type':'success'})
					return redirect('/account/support/'+str(sp_id))
				else:
					flash({'msg':'Wrong catcha, Please try again', 'type':'danger'})
					return redirect('/account/support/'+str(sp_id))      

	return redirect('/account/support/'+str(sp_id))

@support_ctrl.route('/support/new-support-submit', methods=['POST'])
def newsupportsubmit():
	if session.get(u'logged_in') is None:
		flash({'msg':'Please login', 'type':'danger'})
		return redirect('/user/login')
	if request.method == 'POST':
		user_id = session.get('user_id')
		user = db.users.find_one({'_id': ObjectId(user_id)})

		subject = request.form['subject']
		message = request.form['message']
		recaptcha = request.form['g-recaptcha-response']
        if subject == '' or message == '':
            flash({'msg':'Please enter subject or message', 'type':'danger'})
            return redirect('/account/support')
        if recaptcha == '':
            flash({'msg':'Please check captcha', 'type':'danger'})
            return redirect('/account/support')
        else:        
			api_url = 'https://www.google.com/recaptcha/api/siteverify'
			site_key = '6LcESjUUAAAAAN0l4GsSiE2cLLZLZQSRZsEdSroE'
			secret_key = '6LcESjUUAAAAAGsX2iLiwlnbBUyUsZXTz7jrPfAX'
			site_key_post = recaptcha
			ret = urllib2.urlopen('https://api.ipify.org')
			remoteip = ret.read()
			api_url = str(api_url)+'?secret='+str(secret_key)+'&response='+str(site_key_post)+'&remoteip='+str(remoteip);
			response = urllib2.urlopen(api_url)
			response = response.read()
			response = json.loads(response)
			if response['success']:
				data_support = {
				'user_id': user_id,
				'username' : user['username'],
				'message': message,
				'subject': subject,
				'reply': [],
				'date_added' : datetime.utcnow(),
				'status': 0
				}
				db.supports.insert(data_support)
				#flash({'msg':'Success', 'type':'success'})
				return redirect('/account/support')
			else:
				flash({'msg':'Wrong catcha, Please try again', 'type':'danger'})
				return redirect('/account/support')         

	return redirect('/account/support')
