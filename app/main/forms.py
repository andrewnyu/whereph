from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired

class PointSjoinForm(FlaskForm):  
    latitude = StringField(u'Latitude')
    longitude = StringField(u'Longitude')

    submit = SubmitField('Send')