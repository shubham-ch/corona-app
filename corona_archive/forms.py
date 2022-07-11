from ast import Pass
from flask_wtf import FlaskForm

# Linux imports
from wtforms import StringField, SubmitField, PasswordField, FileField
from wtforms.fields.html5 import EmailField


# Windows imports
# from wtforms import StringField, SubmitField, PasswordField, FileField, EmailField

"""
 These classes are used to create form model which are integrated in Register and Login form.
Then the instance are used to validate the inputted data
"""


"""
In case there appears an error while importing EmailField please uncomment the line relevant to your operating systems
"""
from wtforms.validators import DataRequired

class VisitorRegisterForm(FlaskForm):
    full_name = StringField('Full name', validators=[DataRequired()])
    visitor_email = EmailField('Email', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    phone_number = StringField('Phone', validators=[DataRequired()])
    submit = SubmitField('Continue →')

class PlaceRegisterForm(FlaskForm):
    place_name = StringField('Place name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Continue →')

class HospitalLoginForm(FlaskForm):
    hospital_email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login →')

class HospitalRequestForm(FlaskForm):
    hospital_email = EmailField('Email', validators=[DataRequired()])
    submit = SubmitField('Request →')
class AgentLoginForm(FlaskForm):
    agent_email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login →')

class QRCodeUploadForm(FlaskForm):
    file = FileField('QR code', validators=[DataRequired()])
    submit = SubmitField('Check-in →')
class AgentHospitalForm(FlaskForm):
    hospital_email = EmailField('Email', validators=[DataRequired()])
    hospital_pswrd = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('+ Add')
class HospitalInfectCitizen(FlaskForm):
    citizen_ID = StringField('Citizen ID', validators=[DataRequired()])
    submit = SubmitField('Mark Infected')
