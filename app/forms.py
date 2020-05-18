from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import DateField, EmailField
from wtforms.fields import PasswordField, TextAreaField
from wtforms.validators import DataRequired


class EventForm(FlaskForm):
    end_date = DateField('date ', format='%Y-%m-%d', validators=[DataRequired()])
    topic = StringField('topic ')
    text = TextAreaField('text (max 1000 symbols) ')

class CreateUserForm(FlaskForm):
    email = EmailField('E-mail:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])

class LoginForm(FlaskForm):
    email = EmailField('E-mail:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
