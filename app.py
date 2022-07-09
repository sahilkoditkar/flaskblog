
from flask import Flask, render_template, request, redirect, url_for, session
from database import Database
from post import Post
from user import User
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "MyFlaskAPP"

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))

@app.route('/authenticate', methods=['POST'])
def authenticate():
    email = request.form['email']
    password = request.form['password']

    user = User.get_user({'email':email,'password':password})

    if user is None:
        session.pop('email', None)
        return redirect(url_for('login'))
    else:
        session['email'] = email
        return redirect(url_for('home'))

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']

    user = User.get_user({'email':email})

    if user is None:
        user = User(email = email, password = password)
        user.add_user()
        session['email'] = email
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    articles = Post.get_posts()
    return render_template('articles.html', Articles=articles)

@app.route('/article/<id>/')
def article(id):
    article = Post.get_posts({'_id': ObjectId(id)})
    return render_template('article.html', Article = article)

@app.route('/addarticle')
def addarticle():
    return render_template('addarticle.html')

@app.route('/newarticle', methods=['POST'])
def newarticle():
    title = request.form['title']
    content = request.form['content']

    newarticle = Post(author=session['email'], title=title, content=content)
    newarticle.add_post()
    
    return redirect(url_for('articles'))

if __name__ == '__main__':
	app.run(debug=True)