from main import app, quote,render_template,request,redirect, url_for, jsonify,now,auth
from sql_db import News,db,AdminUser as User
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash

from flask_login import login_required, current_user,login_user,logout_user
from flask_login import LoginManager
login_manager = LoginManager()

app.secret_key = 'xxxxyyyyyzzzzz'


db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

class data:
    pass

'''init page'''
@app.route('/')
def index():
    data.current_user = current_user
    return render_template('index.html',data=data)


#page news
@app.route('/news/<url_news>')
def news_get(url_news):
    url_news=(url_news)
    print('url',url_news)
    news = News.query.filter_by(url_news=url_news).first() #(description='There is no data with {}'.format(url_news))
    notice = news.notice
    
    time_read = .5*len(notice.split(' '))
    min=int(time_read//60)
    seg=int(time_read%60)
    
    news.time_read = f'{min if len(str(min))>1 else f"0{min}"}:{seg if len(str(seg))>1 else f"0{seg}"}'
    return render_template('news.html',news=news)


#test db news
@app.route('/db')
def dta():
    return render_template('db.html',data=News.query.all())



# API Publsih
@app.route('/add_news', methods=['GET', 'POST', 'PATCH'])
def question():
    # request.args is to get urls arguments 
    if request.method == 'POST':
        
        title  = request.form['title'] 
        notice  = request.form['news']
        
        url_title = '_tgrth__'
        url_image='gfghkf'
        
        # adding news in db
        date_news=now().strftime('%H:%M:%S %d/%m/%Y')
        url_news=(title)
        news = News(title=title,notice=notice,date=date_news,url_news=url_news)
        
        db.session.add(news)
        db.session.commit()
        data = news
        return redirect(url_for('dta'))
        
    elif request.method == 'GET':
        return jsonify(isError= False,
                    message= "Success",
                    id=news.idNews,
                    statusCode= 200,
                    title=news.title), 200



@app.route('/add_news/<kei>')
def add_news(kei:str):
    if kei=='osvaga':
        return render_template('add_news.html')
    else:
        return '404'


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not (user.password==password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login')) 
    login_user(user, remember=remember)
    return redirect(url_for('profile'))



@app.route('/login')
def login():
    return render_template('login.html')



@app.route('/profile')
@login_required
def profile():
     return render_template('profile.html', name=current_user.email)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/admin')
@login_required
def admin():
    pass