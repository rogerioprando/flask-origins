from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, ValidationError, SelectMultipleField, \
    BooleanField, HiddenField, TextAreaField, SelectField, IntegerField, DateField, FileField

from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileRequired, FileAllowed
from .application import f_images
from .models import AuthApi, User


class LoginForm(FlaskForm):
    email = StringField(u'Email', validators=[DataRequired(u'Informe o e-mail'), Email()])
    password = PasswordField(u'Senha', validators=[DataRequired(u'Informe a senha')])
    remember_me = BooleanField(u'Permanecer logado')


class AuthApiForm(FlaskForm):
    internal = HiddenField()
    client_secret = StringField(u'Client Secret (contexto da rest-api)', validators=[DataRequired(u'Informe o client secret')])
    api_key = StringField(u'API Key (gerado automaticamente)')

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        valid = True

        client = self.check_unique('client_secret')
        if client:
            self.client_secret.errors.append(u'Client Secret já existe')
            valid = False

        return valid

    def check_unique(self, field):
        if field == 'client_secret':
            r_query = AuthApi.query.filter_by(client_secret=self.client_secret.data)

        if self.internal.data:
            r_query = r_query.filter(AuthApi.internal != self.internal.data)

        client = r_query.first()
        return client


class UserEditForm(FlaskForm):
    internal = HiddenField()
    active = BooleanField(u'Ativo', default=True)
    name = StringField(u'Nome Completo', validators=[DataRequired(u'Informe o nome completo')])
    user_email = StringField(u'E-mail',
                             validators=[DataRequired(u'Informe o e-mail'), Email(u'Endereço de e-mail inválido')])
    is_admin = BooleanField(u'Administrador')
    photo = FileField(u'Foto do Perfil', validators=[FileAllowed(f_images, 'Selecione apenas imagens')])
    company = StringField(u'Empresa')
    occupation = StringField(u'Cargo')

    """
    @staticmethod
    def validate_user_email(self, user_email):
        user = User.query.filter_by(user_email=user_email.data).first()
        if user is not None:
            raise ValidationError(u'E-mail informado já utilizado')
    """

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        valid = True

        user = self.check_unique('email')
        if user:
            self.user_email.errors.append(u'E-mail informado já encontra-se cadastrado.')
            valid = False

        return valid

    def check_unique(self, field):
        if field == 'email':
            r_query = User.query.filter_by(user_email=self.user_email.data)

        if self.internal.data:
            r_query = r_query.filter(User.internal != self.internal.data)

        user = r_query.first()
        return user


class UserForm(UserEditForm):
    user_password = PasswordField(u'Senha', validators=[DataRequired(u'Informe uma senha')])
    confirm_password = PasswordField(u'Confirmar Senha', validators=[DataRequired(u'Informe um confirmar senha'),
                                                                     EqualTo('user_password',
                                                                             u'A confirmação de senha não confere')])


class UserChangePasswordForm(FlaskForm):
    current_password = PasswordField(u'Senha Atual', validators=[DataRequired(u'Informe a senha atual')])
    user_password = PasswordField(u'Nova Senha', validators=[DataRequired(u'Informe a nova senha')])
    confirm_password = PasswordField(u'Confirmar Nova Senha', validators=[DataRequired(u'Informe um confirmar senha'),
                                                                     EqualTo('user_password',
                                                                             u'A confirmação de senha não confere')])

