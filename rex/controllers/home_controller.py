from flask import Blueprint, request, session, redirect, url_for, render_template, flash
from flask.ext.login import login_user, logout_user
from rex import app, db
from rex.models import user_model, deposit_model, history_model, invoice_model
import json
from werkzeug.security import generate_password_hash, check_password_hash
__author__ = 'carlozamagni'

home_ctrl = Blueprint('auth', __name__, static_folder='static', template_folder='templates')

def check_password(pw_hash, password):
        return check_password_hash(pw_hash, password)

@home_ctrl.route('/login', methods=['GET', 'POST'])
def home():
    error = None

    return render_template('login.html', error=error)
