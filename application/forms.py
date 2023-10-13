from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, EmailField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo

from application.utils import exists_email, not_exist_email, exists_username


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired(), Length(min=4)])
    password = PasswordField("password", validators=[DataRequired(), Length(min=5)])
    bio      = StringField("bio", validators=[DataRequired()])
    submit   = SubmitField("login")

class SignUpForm(FlaskForm):
    username         = StringField("username", validators=[DataRequired(), Length(min=6)])
    password         = PasswordField("password", validators=[DataRequired(), Length(min=4, max=12)])
    fullname         = StringField("full name", validators=[DataRequired(), Length(min=4, max=16)])
    email            = EmailField("email", validators=[DataRequired(), Email(), exists_email])
    confirm_password = PasswordField("confirm password", validators=[DataRequired(), EqualTo("password", message="password must match")])
    submit           = SubmitField("sign up")  

class EditProfile(FlaskForm):
    username    = StringField("username", validators=[DataRequired(), Length(min=4, max=12), exists_username])
    email       = EmailField("email", validators=[DataRequired(), Email(), exists_email])
    bio         = StringField("bio", validators=[DataRequired()])
    profile_pic = FileField("profile_pic", validators=[FileAllowed(["jpg", "png", "jpeg"])])
    submit      = SubmitField("update profile")

class CreatedPost(FlaskForm):
    photo    = FileField("photo", validators=[DataRequired()])
    caption  = StringField("caption", validators=[DataRequired()])
    submit   = SubmitField("create")

class EditPost(FlaskForm):
    caption  = StringField("caption", validators=[DataRequired(), Length(min=2)])
    submit   = SubmitField("edit")