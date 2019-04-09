from flask import Blueprint, request, session, redirect, url_for, render_template
from flask.ext.login import login_user, logout_user, current_user, login_required
from rex import app, db
from rex.models import user_model, deposit_model, history_model, invoice_model, wallet_model
import json
import urllib
import urllib2
from bson.objectid import ObjectId
import datetime
from datetime import datetime
from datetime import datetime, date, timedelta
from time import gmtime, strftime
import time
import os
import collections
import random
import string
from dateutil.relativedelta import relativedelta
from werkzeug.security import generate_password_hash, check_password_hash
import requests
__author__ = 'carlozamagni'

auto_ctrl = Blueprint('auto', __name__, static_folder='static', template_folder='templates')

