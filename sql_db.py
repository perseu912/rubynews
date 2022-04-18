from main import app
from main import SQLAlchemy
from flask_login import UserMixin

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/ruby_news.db'
db = SQLAlchemy(app)

# app.config['MONGODB_SETTINGS'] = {
#     'db':'ruby_news',
#     'host':'localhost',
#     'port':27017
# }

# db = MongoEngine()
# db.init_app(app)

# db.session.commit()



'''class for the News in db'''
class News(db.Model):
        __tablename__ = 'news'

        id = db.Column(db.Integer,primary_key=True)
        #url_image = db.Column(db.String(20),unique=True,nullable=False)
        title = db.Column(db.String(100),unique=False, nullable=False)
        url_news = db.Column(db.String(40),unique=False,nullable=False)
        notice = db.Column(db.String(2024),unique=False, nullable=False)
        date = db.Column(db.String(20),unique=False, nullable=False)

        def __repr__(self):
                return f'Title news: {self.title}'



class AdminUser(UserMixin,db.Model):
        __tablename__='admin'
        
        id = db.Column(db.Integer,primary_key=True)
        email = db.Column(db.String(40),unique=True,nullable=False)
        password = db.Column(db.String(40),unique=False,nullable=False)
      #  name = db.Column(db.String(10),unique=False,nullable=False)

db.create_all()

# class News(db.Document):
#     title = db.StringField()
#     notice = db.StringField()
#     idNews = db.StringField()


