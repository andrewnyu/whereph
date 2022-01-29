from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField

class LoginForm(FlaskForm):  
    username = StringField(u'Username')
    password = PasswordField(u'Password')

    submit = SubmitField('Log In')