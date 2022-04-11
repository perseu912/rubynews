from flask import Flask, render_template,request
from flask import jsonify
from flask_socketio import SocketIO,emit,send
from json import dump
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from flask_mongoengine import MongoEngine

#from sql import News

#from flask_pymongo import PyMongo



app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/ruby_news.db'
# db = SQLAlchemy(app)

app.config['MONGODB_SETTINGS'] = {
    'db':'ruby_news',
    'host':'localhost',
    'port':27017
}

db = MongoEngine()
db.init_app(app)

# db.session.commit()




# class News(db.Model):
#         __tablename__ = 'news'

#         id = db.Column(db.Integer,primary_key=True)
#         url_image = db.Column(db.String(20),unique=True,nullable=False)
#         title = db.Column(db.String(40),unique=False, nullable=False)
#         url_news = db.Column(db.String(40),unique=False,nullable=False)
#         notice = db.Column(db.String(1024),unique=False, nullable=False)
#         date = db.Column(db.String(20),unique=False, nullable=False)

#         def __repr__(self):
#                 return f'Title news: {self.title}'

class News(db.Document):
    title = db.StringField()
    notice = db.StringField()
    idNews = db.StringField()




#app = Flask(__name__)
#app.config["MONGO_URI"] = "mongodb://localhost:27017/news"
#mongo = PyMongo(app)
bootstrap = Bootstrap5(app)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app,async_mode=None)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/news/<id>')
def news_get(id):
    news = News.objects(id=id).first_or_404() #(description='There is no data with {}'.format(url_news))
    return render_template('news.html',news=news)


@app.route('/db')
def dta():
    return render_template('db.html',data=News.objects)


@app.route('/add_news', methods=['GET', 'POST', 'PATCH'])
def question():
    # request.args is to get urls arguments 
    if request.method == 'GET':
        
        title  = request.args.get('title',type=str)
        notice  = request.args.get('notice',type=str)
        # title  = request.args.get('title',type=str)
        
        url_title = '_tgrth__'
        url_image='gfghkf'
        
        news = News(title=title,notice=notice)
        news.idNews ='qwert'
        
        news.save()
        # questions = mongo.db.questions.find().limit(limit_url).skip(start);
        data = news
        return jsonify(isError= False,
                    message= "Success",
                    id=news.idNews,
                    statusCode= 200,
                    title=news.title), 200

# @app.route('/insta_posts')
# def test():
#     return render_template('insta_posts.html',ca=ca)


###############socket###########
users = {}

@socketio.on('connected')
def connect(data):
    print(data)



@socketio.on('disconnect')
def disconnected(data_):
    print(data_)
    socketio.on('disconnect',data_)

if __name__ == '__main__':
    socketio.run(app,debug=False)