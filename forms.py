from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password')
    ])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class GroupForm(FlaskForm):
    name = StringField('Group Name', validators=[DataRequired()])
    submit = SubmitField('Create Group')

class PromptForm(FlaskForm):
    content = StringField('Prompt', validators=[DataRequired()])
    submit = SubmitField('Add Prompt')

class ResponseForm(FlaskForm):
    answer = TextAreaField('Your Response', validators=[DataRequired()])
    submit = SubmitField('Submit Response')
