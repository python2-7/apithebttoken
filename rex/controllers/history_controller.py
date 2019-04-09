from flask import Blueprint, request, session, redirect, url_for, render_template
from flask.ext.login import login_user, logout_user, current_user, login_required
from rex import app, db
from rex.models import user_model, deposit_model, history_model, invoice_model

__author__ = 'carlozamagni'

history_ctrl = Blueprint('history', __name__, static_folder='static', template_folder='templates')


@history_ctrl.route('/daily-income-history', methods=['GET', 'POST'])
def daily_income_history():
	if session.get(u'logged_in') is None:
		return redirect('/user/login')
	uid = session.get('uid')
	query = db.historys.find({'$and' : [{'type' : 'dailyprofit'},{'uid': uid}]})
	user = db.users.find_one({'customer_id': uid})
	list_notifications = db.notifications.find({'$and' : [{'read' : 0},{'status' : 0},{'$or' : [{'uid' : uid},{'type' : 'all'}]}]})
	number_notifications = list_notifications.count()
	data ={
		'history' : query,
		'title': 'History',
		'menu' : 'history',
		'user': user,
		'number_notifications' : number_notifications,
        'list_notifications' : list_notifications
	}
	return render_template('account/daily_income_history.html', data=data)

@history_ctrl.route('/direct-sales-onus', methods=['GET', 'POST'])
def direct_sales_onus():
	if session.get(u'logged_in') is None:
		return redirect('/user/login')
	uid = session.get('uid')
	query = db.historys.find({'$and' : [{'type' : 'referral'},{'uid': uid}]})
	user = db.users.find_one({'customer_id': uid})
	list_notifications = db.notifications.find({'$and' : [{'read' : 0},{'status' : 0},{'$or' : [{'uid' : uid},{'type' : 'all'}]}]})
	number_notifications = list_notifications.count()
	data ={
		'history' : query,
		'title': 'History',
		'menu' : 'history',
		'user': user,
		'number_notifications' : number_notifications,
        'list_notifications' : list_notifications
	}
	return render_template('account/direct_sales_onus.html', data=data)

@history_ctrl.route('/network-bonus', methods=['GET', 'POST'])
def network_bonus():
	if session.get(u'logged_in') is None:
		return redirect('/user/login')
	uid = session.get('uid')
	query = db.historys.find({'$and' : [{'type' : 'binarybonus'},{'uid': uid}]})
	user = db.users.find_one({'customer_id': uid})
	list_notifications = db.notifications.find({'$and' : [{'read' : 0},{'status' : 0},{'$or' : [{'uid' : uid},{'type' : 'all'}]}]})
	number_notifications = list_notifications.count()
	data ={
		'history' : query,
		'title': 'History',
		'menu' : 'history',
		'user': user,
		'number_notifications' : number_notifications,
        'list_notifications' : list_notifications
	}
	return render_template('account/network_bonus.html', data=data)

@history_ctrl.route('/generations-bonus', methods=['GET', 'POST'])
def generations_bonus():
	if session.get(u'logged_in') is None:
		return redirect('/user/login')
	uid = session.get('uid')
	query = db.historys.find({'$and' : [{'type' : 'generations'},{'uid': uid}]})
	user = db.users.find_one({'customer_id': uid})
	list_notifications = db.notifications.find({'$and' : [{'read' : 0},{'status' : 0},{'$or' : [{'uid' : uid},{'type' : 'all'}]}]})
	number_notifications = list_notifications.count()
	data ={
		'history' : query,
		'title': 'History',
		'menu' : 'history',
		'user': user,
		'number_notifications' : number_notifications,
        'list_notifications' : list_notifications
	}
	return render_template('account/generations_bonus.html', data=data)

@history_ctrl.route('/total-income', methods=['GET', 'POST'])
def total_income():
	if session.get(u'logged_in') is None:
		return redirect('/user/login')
	uid = session.get('uid')
	print uid
	query = db.investments.find({'$and' : [{'status_income' : 1},{'uid': uid}]})
	

	user = db.users.find_one({'customer_id': uid})
	list_notifications = db.notifications.find({'$and' : [{'read' : 0},{'status' : 0},{'$or' : [{'uid' : uid},{'type' : 'all'}]}]})
	number_notifications = list_notifications.count()
	data ={
		'history' : query,
		'title': 'History',
		'menu' : 'history',
		'user': user,
		'number_notifications' : number_notifications,
        'list_notifications' : list_notifications
	}
	return render_template('account/total_income.html', data=data)
