from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from cyber.modules import User

class LoginForm(FlaskForm):
    email       =   StringField("Email", validators=[DataRequired(), Email()])
    # username    =   StringField("Username", validators=[DataRequired()])
    password    =   PasswordField("Password", validators=[DataRequired(), Length(min=6,max=200)])
    remember_me =   BooleanField("Remember Me")
    submit      =   SubmitField("Login")

class RegisterForm(FlaskForm):
    email       =   StringField("Email", validators=[DataRequired(), Email()])
    username    =   StringField("Username", validators=[DataRequired(), Length(min=4,max=25)] )
    password    =   PasswordField("Password", validators=[DataRequired(),Length(min=6,max=200)])
    password_confirm    =   PasswordField("Confirm Password", validators=[DataRequired(),Length(min=6,max=200), EqualTo('password')])
    number_n = IntegerField("Number N", validators=[DataRequired()])
    full_name = StringField("Full Name", validators=[DataRequired(),Length(min=2,max=55)])
    submit = SubmitField("Register Now")

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("This username is already in use. Pick another one.")
    
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email is already in use. Pick another one.")

    
class ResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    number_n = IntegerField("Number N", validators=[DataRequired()])
    password    =   PasswordField("Password", validators=[DataRequired(),Length(min=6,max=200)])
    password_confirm    =   PasswordField("Confirm Password", validators=[DataRequired(),Length(min=6,max=15), EqualTo('password')])
    submit = SubmitField("Reset Now")

