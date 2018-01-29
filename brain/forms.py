from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, ValidationError, SelectMultipleField, \
    BooleanField, HiddenField, TextAreaField, SelectField, IntegerField, DateField, FileField

from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileRequired, FileAllowed
from .application import f_images


class LoginForm(FlaskForm):
    email = StringField(u'Email', validators=[DataRequired(), Email()])
    password = PasswordField(u'Senha', validators=[DataRequired()])
    remember_me = BooleanField(u'Permanecer logado')


class AuthApiForm(FlaskForm):
    pass
