from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email

class UserSignupForm(FlaskForm):
    """form for signing up"""

    username=StringField('Username')
    firstname=StringField('First Name')
    lastname=StringField('Last Name')
    password=PasswordField('Password')

class UserLoginForm(FlaskForm):
    '''form for loggin in'''
    username=StringField('Username')
    password=PasswordField('Password')

class UserReviewForm(FlaskForm):
    '''form for writing a review'''
    title=StringField('Title')
    review=TextAreaField('Review')
# class UserEditForm(FlaskForm):