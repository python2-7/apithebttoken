from flask import Blueprint, request, session, redirect, url_for, render_template
from flask.ext.login import login_user, logout_user, current_user, login_required
from rex import app, db
from rex.models import user_model, deposit_model, history_model, invoice_model

__author__ = 'carlozamagni'

refferal_ctrl = Blueprint('refferal', __name__, static_folder='static', template_folder='templates')

def get_id_tree_node_package(ids):
    listId = 0
    query = db.users.find({'p_node': ids})
    for x in query:
        listId += float(x['investment'])
        listId += get_id_tree_node_package(x['customer_id'])
    return listId

@refferal_ctrl.route('/referrals', methods=['GET', 'POST'])
def refferal():



	if session.get(u'logged_in') is None:
		return redirect('/user/login')
	uid = session.get('uid')
	
	

	user = db.users.find_one({'customer_id': uid})
	username = user['username']
	
	list_notifications = db.notifications.find({'$and' : [{'read' : 0},{'status' : 0},{'$or' : [{'uid' : uid},{'type' : 'all'}]}]})
	number_notifications = list_notifications.count()

	get_id_tree_package = get_id_tree_node_package(uid)

	f1_noactive = db.User.find({'$and' :[{'p_node': uid},{"level": 0}]})
	f1_active_no_tree = db.User.find({'$and' :[{'p_node': uid},{'p_binary' : ''},{"level": { "$gt": 0 }}]})
	f1_active_tree = db.User.find({'$and' :[{'p_node': uid},{ 'p_binary': {'$ne' : ''}},{"level": { "$gt": 0 }}]})

	data ={
		'f1_noactive' : f1_noactive,
		'f1_active_no_tree' : f1_active_no_tree,
		'f1_active_tree' : f1_active_tree,
		'title': 'my-network',
		'menu' : 'my-network',
		'user': user,
		'uid': uid,
		'get_id_tree_package' : get_id_tree_package,
		'number_notifications' : number_notifications,
	    'list_notifications' : list_notifications
	}
	return render_template('account/refferal.html', data=data)
