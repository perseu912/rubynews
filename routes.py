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


'''page news'''
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
        url_news=(title)
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



@app.route('/add_news/<kei>')
def add_news(kei:str):
    if kei=='osvaga':
        return render_template('add_news.html')
    else:
        return '404'
    
# @app.route('/admin')
# def admin():
#     return render_template('/admin/admin.html')

# # @app.route('/insta_posts')
# def test():
#     return render_template('insta_posts.html',ca=ca)

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not (user.password==password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('profile'))


# @app.route('/signup', methods=['POST'])
# def signup_post():
#     email = request.form.get('email')
#     #name = request.form.get('name')
#     password = request.form.get('password')

#     user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

#     if user: # if a user is found, we want to redirect back to signup page so user can try again
#         return redirect(url_for('profile'))

#     # create a new user with the form data. Hash the password so the plaintext version isn't saved.
#     new_user = User(email=email, password=generate_password_hash(password, method='sha256'))

#     # add the new user to the database
#     db.session.add(new_user)
#     db.session.commit()
#     # code to validate and add user to database goes here
#     return redirect(url_for('profile'))




@app.route('/login')
def login():
    return render_template('login.html')

# @app.route('/signup')
# def signup():
#     return render_template('signup.html')


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