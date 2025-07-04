from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'notes_app'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# prevent the db from watching every change which might use a lot of memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __init__(self, username, email, password):
        # take the username given and put it in the username box
        self.username = username
        # take the email given and put it in the email box
        self.email = email
        '''
        take the password given, scramble it into a secret code and
        put it in the password box
        '''
        self.password = generate_password_hash(password)

    def __repr__(self):
        '''
        tells the site how to introduce a user it knows instead of
        just giving type (a User object) and its memory address
        '''
        return f'<User {self.username}>'

    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Both Fields Must Be Filled!", 'danger')
            return redirect(url_for('login'))

        # Add your authentication logic here
        # For now, just redirect to notes
        return redirect(url_for('notes'))
    
    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not username or not email or not password or not confirm_password:
            flash("All Fields Must Be Filled!", 'danger')
            return redirect(url_for('signup'))

        if password != confirm_password:
            flash("Password must match!", 'danger')
            return redirect(url_for('signup'))

        # check uf user already exists using email
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("User Already Exists", 'danger')
            return redirect(url_for('signup'))

        # if everything is new create new user
        try:
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash(f'Account for {new_user} created successfully')
            print(f'New user {new_user} created')
            return redirect(url_for('/'))
        except Exception as e:
            print(f'Error: {e}')
    else:
        print("An error occured!")
    return render_template('signup.html')

@app.route('/')
def notes():
    return render_template('notes.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)