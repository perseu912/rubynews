from flask import Flask, render_template,request, redirect,url_for,flash
from flask import jsonify
from flask_socketio import SocketIO,emit,send
from json import dump
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import datetime as dt
from flask_admin import Admin, AdminIndexView, expose, helpers

from flask_login import current_user

from flask import Blueprint


auth = Blueprint('auth', __name__)



from urllib.parse import quote
now = dt.datetime.now
app = Flask(__name__)

'''the bootstrap init'''
bootstrap = Bootstrap5(app)


# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'


admin = Admin(app, name='RubyNews', template_mode='bootstrap3')


from sql_db import News,db,AdminUser
from flask_admin.contrib.sqla import ModelView


class RubyNewsView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        #flash('ops!')
        return redirect(url_for('login'))


admin.add_view(RubyNewsView(News, db.session))
admin.add_view(RubyNewsView(AdminUser,db.session))