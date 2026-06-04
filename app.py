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
    if 'user' in session:
        return render_template('dashboard.html')
    else:
        return redirect('/login')
    

with app.app_context():
    db.create_all()

app.run(debug=True , port=5001)