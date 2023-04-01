from datetime import datetime
import inspector as inspector
from flask import Flask, render_template, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Date, inspect
from sqlalchemy.orm import sessionmaker, declarative_base
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# *********************************** DATABASE ***************************************** #
# Create the database engine
engine = create_engine('sqlite:///fridge.db', echo=True)
inspector = inspect(engine)
if 'my_table' in inspector.get_table_names():
    print('Table exists')
else:
    print('Table does not exist')

Session = sessionmaker(bind=engine)
Base = declarative_base()

# create flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fridge.db'
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# DATABASE TABLES
class Grocery(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    expiration_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<Grocery(item='{self.item}', quantity='{self.quantity}', expiration_date='{self.expiration_date}')>"

    if not inspector.has_table('item'):
        Base.metadata.create_all(engine)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


# Create the tables in the database
with app.app_context():
    db.create_all()
    db.session.commit()


    # Create a new grocery item
    item1 = Grocery(item_name='Milk', quantity=1, expiration_date=datetime(2022, 4, 1))
    db.session.add(item1)
    db.session.commit()

    # Update the quantity of an existing grocery item
    item2 = Grocery.query.filter_by(item_name='Milk').first()
    item2.quantity = 2
    db.session.commit()

    # Delete a grocery item
    item3 = Grocery.query.filter_by(item_name='Milk').first()
    db.session.delete(item3)
    db.session.commit()






#*********************** FLASK FORMS *************************************#
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
# ********************* FLASK APP ROUTES ************************* #

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        return redirect(url_for('protected'))
    return render_template('login.html', form=form)


@app.route('/add', methods=['POST'])
def add_item():
    # Get the data from the form
    name = request.form['item-name']
    quantity = request.form['quantity']
    expiration_date = datetime.strptime(request.form['expiration-date'], '%Y-%m-%d')

    # Create a new grocery item
    item = Grocery(item_name=name, quantity=quantity, expiration_date=expiration_date)
    db.session.add(item)
    db.session.commit()

    # Redirect to the homepage
    return redirect(url_for('home'))




@app.route('/protected')
def protected():
    return 'This page is protected. You need to be logged in to access it.'

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created for {}!'.format(form.username.data))
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
