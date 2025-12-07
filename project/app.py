from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    usr = db.Column(db.String(80), unique=True, nullable=False)
    pas = db.Column(db.String(120), nullable=False)

@app.route('/')
@app.route('/login')
def login():
    return render_template('auth/login.html')

@app.route('/register')
def register():
    return render_template('auth/register.html')

@app.route('/auth' , methods=['POST'])
def auth():
    action = request.form['action']
    username = request.form['username']
    password = request.form['password']
    if(action == 'register'):
        passwordConfirm = request.form['passwordConfirm']
        if(password != passwordConfirm):
            return "Passwords do not match"
        
        num_upper = sum(1 for c in password if c.isupper())
        num_num = sum(1 for c in password if c.isdigit())
        num_special = sum(1 for c in password if not c.isalnum())
        if(len(username) < 4):
            return "Username must be at least 4 characters long"
        if(len(password) < 8):
            return "Password must be at least 8 characters long"
        if(num_upper < 1):
            return "Password must contain at least one uppercase letter"        
        if(num_num < 1):
            return "Password must contain at least one number"
        if(num_special < 1):
            return "Password must contain at least one special character"
        if(username == password):
            return "Username and password cannot be the same"
        if(User.query.filter_by(usr=username).first()):
            return "Username already exists"
        new_usr = User(usr=username, pas=password)
        db.session.add(new_usr)
        db.session.commit()
        render_template('home.html', username=username)
    elif(action == 'login'):
        if(not User.query.filter_by(usr=username, pas=password).first()):
            return "Invalid username or password"
        else:
            return render_template('home.html', username=username)
    return "Error"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)