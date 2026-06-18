from flask import Flask,   redirect, render_template , request,session ,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "mysecretkey"

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model ):
    sno = db.Column(db.Integer, primary_key=True)           
    Username = db.Column(db.String(200), nullable=False)
    Password = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class Post(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    title = db.Column(db.String ,nullable=False)
    content = db.Column(db.String , nullable=False)
    author = db.Column(db.String , nullable=False)
    category = db.Column(db.String(100), default="General")
    date_created = db.Column(db.DateTime , default=datetime.utcnow)
    
class Comment(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    content = db.Column(db.String , nullable=False)
    author = db.Column(db.String , nullable=False)
    post_id = db.Column(db.Integer , nullable=False)
    date_created = db.Column(db.DateTime ,  default=datetime.utcnow)

@app.route('/' , methods=['GET', 'POST'])
def home():

    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(Username=username).first()

        if user and user.Password == password:
            session['user'] = username
            return redirect('/dashboard')

        else:
            flash("Invalid username or password")
            return redirect('/')

    return render_template('auth/login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        new_user = User(Username=username, Password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect('login')

    return render_template('auth/signup.html')

@app.route('/dashboard')
def dashboard():

    if 'user' not in session:
        return redirect('/login')

    posts = Post.query.filter_by(author=session['user']).all()

    return render_template('blog/dashboard.html', posts=posts)
    
@app.route('/create_post', methods=['GET', 'POST'])
def create_post():

    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form['category']

        new_post = Post(
            title=title,
            content=content,
            author=session['user'],
            category=category
        )

        db.session.add(new_post)
        db.session.commit()

        return redirect('/dashboard')

    return render_template('blog/create_post.html')
    
@app.route('/my_post')
def my_post():

    if 'user' not in session:
        return redirect('/login')

    posts = Post.query.filter_by(author=session['user']).all()

    return render_template('blog/my_post.html', posts=posts)

@app.route('/all_post')
def all_post():

    if 'user' not in session:
        return redirect('/login')

    posts = Post.query.all()

    return render_template('blog/all_post.html', posts=posts)

@app.route('/profile')
def profile():

    if 'user' not in session:
        return redirect('/login')

    user = User.query.filter_by(Username=session['user']).first()

    total_posts = Post.query.filter_by(author=session['user']).count()

    return render_template(
        'blog/profile.html',
        user=user,
        total_posts=total_posts
    )

@app.route('/delete_post/<int:id>')
def delete_post(id):

    if 'user' not in session:
        return redirect('/login')

    post = Post.query.get_or_404(id)

    if post.author != session['user']:
        return redirect('/my_post')

    db.session.delete(post)
    db.session.commit()

    return redirect('/my_post')

@app.route('/edit_post/<int:id>', methods=['GET', 'POST'])
def edit_post(id):

    if 'user' not in session:
        return redirect('/login')

    post = Post.query.get_or_404(id)

    if post.author != session['user']:
        return redirect('/my_post')

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']

        db.session.commit()

        return redirect('/my_post')

    return render_template('blog/edit_post.html', post=post)

@app.route('/logout')
def logout():

    if 'user' not in session:
        return redirect('/login')

    session.pop('user', None)

    return redirect('/login')

@app.route('/post/<int:id>', methods=['GET', 'POST'])
def post_detail(id):

    post = Post.query.get_or_404(id)

    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':

        content = request.form['comment']

        comment = Comment(
            content=content,
            author=session['user'],
            post_id=id
        )

        db.session.add(comment)
        db.session.commit()

        return redirect(f'/post/{id}')

    comments = Comment.query.filter_by(post_id=id).all()

    return render_template(
        'blog/post_detail.html',
        post=post,
        comments=comments
    )  

@app.route('/delete_comment/<int:id>')
def delete_comment(id):

    if 'user' not in session:
        return redirect('/login')
    
    comment = Comment.query.get_or_404(id)

    if comment.author != session['user']:
        return redirect(f'/post/{comment.post_id}')
    
    db.session.delete(comment)
    db.session.commit()

    return redirect(f'/post/{comment.post_id}')


@app.route('/search', methods=['GET', 'POST'])
def search():

    if 'user' not in session:
        return redirect('/login')

    q = request.args.get('q')

    posts = Post.query.filter(Post.title.contains(q)).all()

    return render_template('blog/search.html', posts=posts)



@app.route('/category/<category_name>')
def category_posts(category_name):

    if 'user' not in session:
        return redirect('/login')

    posts = Post.query.filter_by(category=category_name).all()

    return render_template(
        'blog/category_posts.html',
        posts=posts,
        category=category_name
    )

@app.route('/setting' , methods=['GET', 'POST'])
def setting():

    if 'user' not in session:
        return redirect('/login')

    return render_template('blog/setting.html')
    
with app.app_context():
    db.create_all()

app.run(debug=True , port=5001)