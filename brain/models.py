from flask_login import UserMixin
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from .application import db, login_manager
from flask_uuid import uuid


class AuthApi(db.Model):
    __tablename__ = 'xf_auth_api'

    internal = db.Column(db.String(200), primary_key=True, default=uuid.uuid4())
    created = db.Column(db.DateTime, default=datetime.utcnow())
    client_secret = db.Column(db.String(), nullable=False, unique=True)
    api_key = db.Column(db.String(), nullable=False, unique=True)


class LoginActivity(db.Model):
    __tablename__ = 'xf_login_activities'

    internal = db.Column(db.String(200), primary_key=True, default=uuid.uuid4())
    created = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('xf_user.id'))
    user = db.relationship('User', backref=db.backref('activities', cascade='all, delete-orphan'), lazy='joined')
    action = db.Column(db.String(), nullable=False)
    ip_address = db.Column(db.String(), nullable=False)
    ua_header = db.Column(db.String(), nullable=False)
    ua_device = db.Column(db.String(), nullable=False)


class User(UserMixin, db.Model):
    __tablename__ = 'xf_user'

    id = db.Column(db.Integer, primary_key=True)
    internal = db.Column(db.String(200), index=True, unique=True, default=uuid.uuid4())
    created = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean, nullable=False, default=False)
    name = db.Column(db.String(200), nullable=False)
    user_name = db.Column(db.String(100), index=True, unique=True)
    user_email = db.Column(db.String(200), index=True, unique=True)
    user_password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    file_name = db.Column(db.String())
    file_url = db.Column(db.String())
    company = db.Column(db.String())
    occupation = db.Column(db.String())

    @property
    def password(self):
        # Prevent password from being accessed
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.user_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.user_password, password)

    @classmethod
    def from_dict(cls, provider_dict):
        id = provider_dict.get('id')
        internal = provider_dict.get('internal')
        created = provider_dict.get('created')
        active = provider_dict.get('active')
        name = provider_dict.get('name')
        user_name = provider_dict.get('user_email').lower()
        user_email = provider_dict.get('user_email').lower()
        user_password = provider_dict.get('user_password')
        is_admin = provider_dict.get('is_admin')
        file_name = provider_dict.get('file_name')
        file_url = provider_dict.get('file_url')
        company = provider_dict.get('company')
        occupation = provider_dict.get('occupation')

        return User(id=id,
                    internal=internal,
                    created=created,
                    active=active,
                    name=name,
                    user_name=user_name,
                    user_email=user_email,
                    password=user_password,
                    is_admin=is_admin,
                    file_name=file_name,
                    file_url=file_url,
                    company=company,
                    occupation=occupation)

    def __repr__(self):
        return '<User: {}>'.format(self.user_name)


@login_manager.user_loader
def load_user(user_id):
    """
        load user from database to session, using Flask Login
    """
    return User.query.get(int(user_id))
