from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, EmailField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo

from application.utils import exists_email, not_exists_email, exists_username
    

class LoginForm(FlaskForm):
    username            = StringField("Username", validators=[DataRequired()])
    password            = PasswordField("Password", validators=[DataRequired()])
    submit              = SubmitField("Login")

class SignUpForm(FlaskForm):
    username            = StringField("Username", validators=[DataRequired(), Length(min=4, max=12), exists_username])
    fullname            = StringField("Full name", validators=[DataRequired(), Length(min=4, max=16)])
    email               = EmailField("Email", validators=[DataRequired(), Email(), exists_email])
    password            = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password    = PasswordField("Confirm password", validators=[DataRequired(), Length(min=6), EqualTo("password")])
    submit              = SubmitField("Sign up")

class EditProfileForm(SignUpForm):
    username            = StringField("Username", validators=[DataRequired(), Length(min=4, max=12)])
    password            = None
    confirm_password    = None
    email               = EmailField("E-mail", validators=[DataRequired(), Email(), exists_email])
    bio                 = StringField("Bio")
    profile_pic         = FileField("Profile picture", validators=[FileAllowed(["jpg", "png", "jpeg"])])
    submit              = SubmitField("Update profile")

class ResetPasswordForm(FlaskForm):
    old_password         = PasswordField("Old password", validators=[DataRequired(), Length(min=6)])
    new_password         = PasswordField("New password", validators=[DataRequired(), Length(min=6)])
    confirm_new_password = PasswordField("Confirm new password", validators=[DataRequired(), Length(min=6), EqualTo("new_password")])
    submit               = SubmitField("Reset password")

class ForgotPasswordForm(FlaskForm):
    email               = EmailField("Email", validators=[DataRequired(), not_exists_email])
    # recaptcha           = RecaptchaField()
    submit              = SubmitField("Send link verification to email")

class VerificationResetPasswordForm(FlaskForm):
    password            = PasswordField("New password", validators=[DataRequired(), Length(min=6)])
    confirm_password    = PasswordField("Confirm new password", validators=[DataRequired(), Length(min=6), EqualTo("password")])
    submit              = SubmitField("Reset password")

class CreatePostForm(FlaskForm):
    post_pic            = FileField("Picture", validators=[DataRequired(), FileAllowed(["jpg", "png", "jpeg"])])
    caption             = TextAreaField("Caption")
    submit              = SubmitField("Post")

class EditPostForm(FlaskForm):
    caption             = StringField("Caption")
    submit              = SubmitField("Update post")