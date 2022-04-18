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

# from flask_mongoengine import MongoEngine

#from sql import News

#from flask_pymongo import PyMongo

# from flask_login import LoginManager


app = Flask(__name__)

#app = Flask(__name__)
#app.config["MONGO_URI"] = "mongodb://localhost:27017/news"
#mongo = PyMongo(app)

'''the bootstrap init'''
bootstrap = Bootstrap5(app)


# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'


# login_manager = LoginManager(app)
# login_manager.session_protection = 'strong'
# login_manager.login_view = 'admin.login'

admin = Admin(app, name='RubyNews', template_mode='bootstrap3')


from sql_db import News,db,AdminUser
from flask_admin.contrib.sqla import ModelView



# class RubyNewsView(ModelView):
#     can_delete = True # disable model deletion
#     page_size = 50  # the number of entries to display on the list view
#     can_create = True
#     can_edit = True
#     can_delete = True
#     column_editable_list = ['title', 'news']


# class FlaskyAdminIndexView(AdminIndexView):

#     @expose('/')
#     def index(self):
#         if not login.current_user.is_authenticated:
#             return redirect(url_for('.login'))
#         return super(MyAdminIndexView, self).index()

#     @expose('/login', methods=['GET', 'POST'])
#     def login(self):
#         form = LoginForm(request.form)
#         if helpers.validate_form_on_submit(form):
#             user = form.get_user()
#             if user is not None and user.verify_password(form.password.data):
#                 login.login_user(user)
#             else:
#                 flash('Invalid username or password.')
#         if login.current_user.is_authenticated:
#             return redirect(url_for('.index'))
#         self._template_args['form'] = form
#         return super(MyAdminIndexView, self).index()

#     @expose('/logout')
#     @login_required
#     def logout(self):
#         login.logout_user()
#         return redirect(url_for('.login'))

class RubyNewsView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        #flash('ops!')
        return redirect(url_for('login'))


admin.add_view(RubyNewsView(News, db.session))
admin.add_view(RubyNewsView(AdminUser,db.session))