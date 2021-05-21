from flask import Flask, request
from flask_wtf import FlaskForm
from flask import render_template
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from test import send_message
from regexx import cancities

class Config(object):
    SECRET_KEY = 'Hello'


class LoginForm(FlaskForm):
    username = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])

    location = StringField('Location', validators=[DataRequired()])
    
    password = StringField('Phone Number', validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    permission = BooleanField('Permission', validators=[DataRequired()])

    submit = SubmitField('Sign In')


app = Flask(__name__,static_url_path='/static')
app.config.from_object(Config)
Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def hello():

    cities = cancities
    return render_template('new.html', title='Vaxx',cities=cities)


@app.route('/submitted',methods=['POST'])
def submitted():

    print(request.form)
    if len(request.form.getlist("perm")) == 0:
        return "Permission Was Denied"
    
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    phoneNumber = request.form['phone']
    age = request.form['age']
    location = request.form['cityPicker']
    send_message(firstName + " " + lastName, phoneNumber, location, age)
    return "Check your phone for a confirmation SMS"
# Keep this at the bottom of app.py
app.run(debug=True)
