from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField

class PointSjoinForm(FlaskForm):  
    latitude = StringField(u'Latitude')
    longitude = StringField(u'Longitude')

    submit = SubmitField('Send')