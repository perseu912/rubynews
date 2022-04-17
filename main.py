from flask import Flask, render_template,request, redirect,url_for
from flask import jsonify
from flask_socketio import SocketIO,emit,send
from json import dump
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import datetime as dt

from urllib.parse import quote
now = dt.datetime.now

from flask_mongoengine import MongoEngine

#from sql import News

#from flask_pymongo import PyMongo



app = Flask(__name__)

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




class News(db.Model):
        __tablename__ = 'news'

        id = db.Column(db.Integer,primary_key=True)
        #url_image = db.Column(db.String(20),unique=True,nullable=False)
        title = db.Column(db.String(40),unique=False, nullable=False)
        url_news = db.Column(db.String(40),unique=False,nullable=False)
        notice = db.Column(db.String(1024),unique=False, nullable=False)
        date = db.Column(db.String(20),unique=False, nullable=False)

        def __repr__(self):
                return f'Title news: {self.title}'

db.create_all()
'''class for the News in db'''
# class News(db.Document):
#     title = db.StringField()
#     notice = db.StringField()
#     idNews = db.StringField()




#app = Flask(__name__)
#app.config["MONGO_URI"] = "mongodb://localhost:27017/news"
#mongo = PyMongo(app)

'''the bootstrap init'''
bootstrap = Bootstrap5(app)


app.config['SECRET_KEY'] = 'secret!'

'''the scoketio init'''
socketio = SocketIO(app,async_mode=None)


'''init page'''
@app.route('/')
def index():
    return render_template('index.html')


'''page news'''
@app.route('/news/<url_news>')
def news_get(url_news):
    url_news=quote(url_news)
    print('url',url_news)
    news = News.query.filter_by(url_news=url_news).first() #(description='There is no data with {}'.format(url_news))
    return render_template('news.html',news=news)


'''test db page'''
@app.route('/db')
def dta():
    return render_template('db.html',data=News.query.all())



'''to publish API'''
@app.route('/add_news', methods=['GET', 'POST', 'PATCH'])
def question():
    # request.args is to get urls arguments 
    if request.method == 'POST':
        
        title  = request.form['title'] #,type=str) #getting the title news
        notice  = request.form['news']#,type=str) #getting the notice news
        # title  = request.args.get('title',type=str)
        
        url_title = '_tgrth__'
        url_image='gfghkf'
        
        # adding news in db
        date_news=now().strftime('%H:%M:%S %d/%m/%Y')
        url_news=quote(title)
        news = News(title=title,notice=notice,date=date_news,url_news=url_news)
        #news.idNews ='qwert'
        
        #save news in db
        #news.save()
        db.session.add(news)
        db.session.commit()
        # questions = mongo.db.questions.find().limit(limit_url).skip(start);
        data = news
        return redirect(url_for('dta'))
        
    elif request.method == 'GET':
        return jsonify(isError= False,
                    message= "Success",
                    id=news.idNews,
                    statusCode= 200,
                    title=news.title), 200



'''page admin'''
password='osvaga'
user='rey'
@app.route('/admin/<kei>')
def admin(kei:str):
    if kei==password:
        return render_template('admin.html')
    else:
        return '404'

# @app.route('/insta_posts')
# def test():
#     return render_template('insta_posts.html',ca=ca)


###############socket###########
users = {}


# connected
@socketio.on('connected')
def connect(data):
    print(data)


#disconnected
@socketio.on('disconnect')
def disconnected(data_):
    print(data_)
    socketio.on('disconnect',data_)


#run
if __name__ == '__main__':
    socketio.run(app,debug=False)