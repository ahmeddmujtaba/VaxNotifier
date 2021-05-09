from flask import Flask
from flask_wtf import FlaskForm
from flask import render_template
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import phonenumbers
from test import send_message


class Config(object):
    SECRET_KEY = 'Hello'


class LoginForm(FlaskForm):
    username = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])

    location = StringField('Location', validators=[DataRequired()])
    
    password = StringField('Phone Number', validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])

    submit = SubmitField('Sign In')


app = Flask(__name__)
app.config.from_object(Config)
Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def hello():
    form = LoginForm()
    if form.validate_on_submit():

        print(form.username.data)
        print(form.lastName.data)
        print(form.password.data)
        print(form.age.data)
        send_message(form.username.data + " " + form.lastName.data, form.password.data,form.location.data,form.age.data)

    return render_template('index.html', title='Vaxx', form=form)


# Keep this at the bottom of app.py
app.run(debug=True)
