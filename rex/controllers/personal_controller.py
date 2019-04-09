from flask import Blueprint, request, session, redirect, url_for, render_template
from flask.ext.login import login_user, logout_user, current_user, login_required
from rex import app, db
import json
from rex.models import user_model, deposit_model, history_model, invoice_model
from bson import ObjectId, json_util
__author__ = 'carlozamagni'

personal_ctrl = Blueprint('personal', __name__, static_folder='static', template_folder='templates')
def format_date(date): # date = datetime object.
    return date.strftime('%Y-%m-%d')

def format_satoshi(value):
    value = float(value)
    return '{:20,.2f}'.format(value)
def format_usd(value):
    value = float(value)
    return '{:20,.2f}'.format(value)

def number_format(value, tsep=',', dsep='.'):
    s = unicode(value)
    cnt = 0
    numchars = dsep + '0123456789'
    ls = len(s)
    while cnt < ls and s[cnt] not in numchars:
        cnt += 1

    lhs = s[:cnt]
    s = s[cnt:]
    if not dsep:
        cnt = -1
    else:
        cnt = s.rfind(dsep)
    if cnt > 0:
        rhs = dsep + s[cnt+1:]
        s = s[:cnt]
    else:
        rhs = ''

    splt = ''
    while s != '':
        splt = s[-3:] + tsep + splt
        s = s[:-3]

    return lhs + splt[:-1] + rhs
def reduceTree (user):
    json = []
    sponser = db.users.find_one({'customer_id': user['p_node']})
    if sponser is not None:
        user_sponser = sponser['username']
    else:
        user_sponser = "administrator"

   
    levelss = user['level']

    tree = {
        "id":user['customer_id'],
        "text":str(user['username'].encode('utf-8')),
        "username":str(user['username'].encode('utf-8')),
        "email":user['email'],
        "date_added":format_date(user['creation']),
        "level":levelss,
        
        "leftPD":format_usd(user['total_pd_left']),
        "rightPD":format_usd(user['total_pd_right']),
        "totalPD":format_usd(user['investment']),
        "sponsor":user_sponser,
        "empty":False,
        "iconCls":"level2",
        "fl":1,
        'children' : []
    }
    json.append(tree)
    children_tree(tree)
    
    return json
def children_tree (json):
    customer = db.users.find_one({'customer_id': json['id']})
    user_p_left = db.users.find_one({"$and" :[{'p_binary': json['id']}, {'customer_id': customer['left']}] })
    # import pdb
    # pdb.set_trace()
    if user_p_left is not None:



        user_sponser_left =  db.users.find_one({'customer_id': user_p_left['p_node']})

        fl = json['fl'] + 1
        
        levelss_left = user_p_left['level']
        tree = {
            "id":user_p_left['customer_id'],
            "text":str(user_p_left['username'].encode('utf-8')),
            "username":str(user_p_left['username'].encode('utf-8')),
            "email":str(user_p_left['email'].encode('utf-8')),
            
            "date_added":format_date(user_p_left['creation']),
            "level":levelss_left,
            "level_user":"Null",
            "leftPD":format_usd(user_p_left['total_pd_left']),
            "rightPD":format_usd(user_p_left['total_pd_right']),
            "totalPD":format_usd(user_p_left['investment']),
            "sponsor":user_sponser_left['username'],
            "empty":False,
            "iconCls":"level2 left",
            "status" : 1,
            "fl":fl,
            'children' : []
        }
        if fl < 5:
            json['children'].append(tree)
            children_tree(tree)
    else:
        fl = json['fl'] + 1
        tree = {  
            "fl":fl,
            "p_binary":json['id'],
            "empty":True,
            "iconCls":"level1 left",
            "id":"-1"
        }
        if fl < 5:
            json['children'].append(tree)

    
    user_p_right = db.users.find_one({"$and" :[{'p_binary': json['id']}, {'customer_id': customer['right']}] })
    if user_p_right is not None:

        user_sponser_right = db.users.find_one({'customer_id': user_p_right['p_node']})
        fl = json['fl'] + 1
        
        levelss_right = user_p_right['level']
        tree = {
            "id":user_p_right['customer_id'],
            "text":str(user_p_right['username'].encode('utf-8')),
            "username":str(user_p_right['username'].encode('utf-8')),
            "email":str(user_p_right['email'].encode('utf-8')),
            "date_added":format_date(user_p_right['creation']),
            
            "level":levelss_right,
            "level_user":"Null",
            "leftPD":format_usd(user_p_right['total_pd_left']),
            "rightPD":format_usd(user_p_right['total_pd_right']),
            "totalPD":format_usd(user_p_right['investment']),
            "sponsor":user_sponser_right['username'],
            "empty":False,
            "iconCls":"level2 right",
            "status" : 1,
            "fl":fl,
            'children' : []
        }
        if fl < 5:
            json['children'].append(tree)
            children_tree(tree)
    else:
        fl = json['fl'] + 1
        tree = {  
            "fl":fl,
            "p_binary":json['id'],
            "empty":True,
            "iconCls":"level1 right",
            "id":"-1"
        }
        if fl < 5:
            json['children'].append(tree)

    return json 

def renderJson(uid) :
    user = db.users.find_one({'customer_id': uid})
    return reduceTree(user)

def get_id_tree(ids):
    listId = ''

    query = db.users.find({'p_binary': ids})
    for x in query:
        listId += ', %s'%(x['customer_id'])
        listId += get_id_tree(x['customer_id'])
    return listId

def total_binary_left(customer_id):
    customer = db.users.find_one({'customer_id': customer_id})
    count_left = 0
    if customer['left'] == '':
        count_left = 0
    else:
        id_left_all = str(customer['left'])+get_id_tree(customer['left'])
        id_left_all = id_left_all.split(',')
        if (len(id_left_all) > 0):
            for yy in id_left_all:
                count_left = count_left + 1
    return count_left

def total_binary_right(customer_id):
    customer = db.users.find_one({'customer_id': customer_id})
    count_right = 0
    if customer['right'] == '':
        count_right = 0
    else:
        id_right_all = str(customer['right'])+get_id_tree(customer['right'])
        id_right_all = id_right_all.split(',')
        if (len(id_right_all) > 0):
            for yy in id_right_all:
                count_right = count_right + 1
    return count_right

@personal_ctrl.route('/network-tree', methods=['GET', 'POST'])
def personal():
    if session.get(u'logged_in') is None:
        return redirect('/user/login')
    
    uid = session.get('uid')
    user = db.users.find_one({'customer_id': uid})
    username = user['username']
    total_binary_lefts =  total_binary_left(uid)
    total_binary_rights =  total_binary_right(uid)

    count_f1 = db.User.find({'$and' :[{'p_node': uid},{"level": { "$gt": 0 }}]}).count()


    list_notifications = db.notifications.find({'$and' : [{'read' : 0},{'status' : 0},{'$or' : [{'uid' : uid},{'type' : 'all'}]}]})
    number_notifications = list_notifications.count()

    values = {
        'uid' : uid,
        'user' : user,
        'float':float,
        'menu':'network-tree',
        'total_binary_left' : total_binary_lefts,
        'total_binary_right' : total_binary_rights,
        'count_f1' : count_f1,
        'number_notifications' : number_notifications,
        'list_notifications' : list_notifications
    }
    return render_template('account/personal.html', data=values)
@personal_ctrl.route('/count-binary', methods=['GET', 'POST'])
def countBinary():
    if session.get(u'logged_in') is None:
        return json.dumps({'status' : 'error', "msg": "Please login"})
    uid = session.get('uid')
    customer = db.trees.find_one({'customer_id': uid})
    user = db.users.find_one({'customer_id': uid})
    if customer is None:
        count_left = total_binary_left(uid)
        count_right = total_binary_right(uid)
        data_tree = {
        'customer_id' : uid,
        'count_left' : count_left,
        'count_right': count_right,
        'username' : user['username']
        }
        db.trees.insert(data_tree)
        values = {
            'total_binary_right': count_right,
            'total_binary_left': count_left
        }
    else:
        values = {
            'total_binary_right': customer['count_right'],
            'total_binary_left': customer['count_left']
        }
    return json.dumps(values)
@personal_ctrl.route('/calculatorBinary', methods=['GET', 'POST'])
def calculatorBinary():
    if session.get(u'logged_in') is None:
        return json.dumps({'status' : 'error', "msg": "Please login"})
    uid = session.get('uid')
    customer = db.trees.find_one({'customer_id': uid})
    user = db.users.find_one({'customer_id': uid})
    if customer is None:
        return json.dumps({'status': 'success'})
    else:
        count_left = total_binary_left(uid)
        count_right = total_binary_right(uid)
        db.trees.update({ "customer_id" : uid, 'username': user['username'] }, { '$set': {"count_left": count_left, "count_right": count_right } })        
    return json.dumps({'status': 'success'})

def get_id_tree_left(ids):
    listId = ''
    query = db.users.find({'customer_id': ids})
    for x in query:
        listId += ', %s'%(x.left)
        listId += get_id_tree_left(x.left)
    return listId
def get_id_tree_right(ids):
    listId = ''
    query = db.users.find({'customer_id': ids})
    for x in query:
        print x['right']
        listId += ', %s'%(x.right)
        listId += get_id_tree_right(x.right)
    return listId

def Get_binary_binary_left(customer_id):
    count = db.users.find_one({'customer_id': customer_id})
    customer_binary =''
    if count.left == '':
        customer_binary += ', %s'%(customer_id)
    else:
        ids = count.left
        count = get_id_tree_left(count.left)
        if count:
            customer_binary = '%s , %s'%(count, ids)
        else:
            customer_binary = ',%s'%(ids)
    customer_binary = customer_binary[1:]
    customers = customer_binary.split(',')

    if len(customers)== 2:
        customer_binary = customers[1].strip()
    if len(customers) >= 3:
        customer_binary = max(customers).strip()
    return customer_binary
def Get_binary_binary_right(customer_id):
    count = db.users.find_one({'customer_id': customer_id})
    customer_binary =''
    if count.right == '':
        customer_binary += ', %s'%(customer_id)
    else:
        ids = count.right
        count = get_id_tree_right(count.right)
        if count:
            customer_binary = '%s , %s'%(count, ids)
        else:
            customer_binary = ',%s'%(ids)
    customer_binary = customer_binary[1:]
    customers = customer_binary.split(',')
    print customers
    if len(customers)== 2:
        customer_binary = customers[1].strip()
    if len(customers) >= 3:
        customer_binary = max(customers).strip()
    return customer_binary
def get_id_in_binary(uid):
    listId =''
    ListUser = db.users.find({'p_binary': uid})
    for x in ListUser:
        listId += ',%s'%(x['customer_id'])
        listId += str(get_id_in_binary(x['customer_id']))
    return listId


@personal_ctrl.route('/SearchTree', methods=['GET', 'POST'])
def SearchTree():
    # return json.dumps({ 'status': 'error', 'message': 'Please enter username' })
    # if session.get(u'logged_in') is None:
    #     return json.dumps({
    #         'status': 'error', 
    #         'message': 'Please login'
    #     })
    uid = request.form['uid']
    if request.method == 'POST':
        username = request.form['username']
        if username == '':
            return json.dumps({
                'status': 'error', 
                'message': 'Please enter username',
                'uid': uid
            })
        username = username.lower()
        findUser = db.users.find_one({'username': username})
        if findUser is None:
            return json.dumps({
                'status': 'error', 
                'message': 'Username dose not exits',
                'uid': uid
            })
        ListID = get_id_in_binary(uid)
        ListID = ListID[1:]
        ListID = ListID.split(',')
        if findUser['customer_id'] in ListID:
            return json.dumps({
                'status': 'success', 
                'message': '',
                'uid': findUser['customer_id']
            })
        else:
            return json.dumps({
                'status': 'error', 
                'message': 'Username dose not exits',
                'uid': uid
            })
        
    else:
        return json.dumps({
            'status': 'error', 
            'message': 'Only Post'
        })
   

@personal_ctrl.route('/json_tree', methods=['GET', 'POST'])
def json_tree():
    if request.method == 'POST':
        # if session.get(u'logged_in') is not None:
        uid = request.form['id_user']
        
        page_sanitized = json_util.dumps(renderJson(uid))
        return page_sanitized
    else:
        return json.dumps({
                'status': 'error'
            })

@personal_ctrl.route('/teamnetworksummary', methods=['GET', 'POST'])
def teamnetworksummary():
    if session.get(u'logged_in') is None:
        return redirect('/user/login')
    uid = session.get('uid')
    refferal_link = 'http://%s/user/register/%s' % (request.host,uid)
    user = db.users.find_one({'customer_id': uid})
    values = {
        'refferal_link' : refferal_link,
        'uid' : uid,
        'user' : user,
        'float':float
    }
    return render_template('account/summary.html', data=values)
@personal_ctrl.route('/tree-system', methods=['GET', 'POST'])
def personal_tree():
    if session.get(u'logged_in') is None:
        return redirect('/user/login')
    user_id = session.get('user_id')
    uid = session.get('uid')
    user = db.users.find_one({'customer_id': uid})
    username = user['username']
    refferal_link = 'https://worldtrader.info/user/register/%s' % (user['customer_id'])
    user = db.users.find_one({'customer_id': uid})
    values = {
        'refferal_link' : refferal_link,
        'uid' : uid,
        'user' : user,
        'float':float,
        'menu':'personal_ico',
        'uid': uid
    }
    return render_template('account/tree_ico.html', data=values)
def reduceTree_ico(user):
    json = []
    tree = {
        "id":str(user['customer_id']),
        # "text":str(user['username']) +" (Invest: $" +str(user['total_invest'])+")",
        "text":'<img src="/static/img/package/package-'+str(int(user['level']))+'.png" alt="" class="img_tree_s">'+str(user['username']),
        "empty":False,
        "iconCls":"level2",
        "fl":1,
        'children' : []
    }

    json.append(tree)
    children_tree_ico(tree)
    return json
def children_tree_ico(json):
    customer = db.users.find({'p_node': json['id']}, {'username':1, 'investment': 1, 'customer_id': 1, 'level': 1})
    if customer:
        for x in customer:
            checkF1 = db.users.find({'p_node': str(x['customer_id'])}).count()
            
            if int(checkF1) > 0:
                dataChild = True
            else:
                dataChild = ''
            tree = {
                "id":str(x['customer_id']),
                # "text":str(x['username'])+" (Invest: $" +str(x['total_invest'])+")",
                "text":'<img src="/static/img/package/package-'+str(int(x['level']))+'.png" alt="" class="img_tree_s">'+str(x['username']),
                "empty":False,
                "iconCls":"level2",
                "fl":1,
                'children' : dataChild
            }
            json['children'].append(tree)
            # children_tree_ico(tree)
    else:
        json['children']=0
    return json
def renderJson_ico(uid):
    user = db.users.find_one({'customer_id': uid}, {'username': 1, 'investment':1, 'customer_id': 1, 'level': 1})
    return reduceTree_ico(user)
@personal_ctrl.route('/json_tree_ico/<uid>', methods=['GET', 'POST'])
def json_tree_ico(uid):
    id_request =  request.args.get('id')
    if id_request == '#':
        uid = str(uid)
    else:
        uid = str(id_request)
    page_sanitized = json_util.dumps(renderJson_ico(uid))
    return page_sanitized



@personal_ctrl.route('/add-tree/<p_binary>/<position>', methods=['GET', 'POST'])
def personaladdtree(p_binary,position):
    if session.get(u'logged_in') is None:
        return redirect('/user/login')
    
    uid = session.get('uid')
    user = db.users.find_one({'customer_id': uid})
    
    query = db.User.find({'$and' :[{'p_node': uid},{'p_binary' : ''},{"level": { "$gt": 0 }}]})
    checkF1 = True
    list_notifications = db.notifications.find({'$and' : [{'read' : 0},{'status' : 0},{'$or' : [{'uid' : uid},{'type' : 'all'}]}]})
    number_notifications = list_notifications.count()
    if query.count() == 0:
        checkF1 = False
    values = {
        'uid' : uid,
        'user' : user,
        'float':float,
        'len' : len,
        'menu':'network-tree',
        'refferal' : query,
        'p_binary' : p_binary,
        'position' : position,
        'checkF1' : checkF1,
        'number_notifications' : number_notifications,
        'list_notifications' : list_notifications
    }
    return render_template('account/add-tree.html', data=values)