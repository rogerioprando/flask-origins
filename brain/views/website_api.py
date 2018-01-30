import uuid

from flask import Blueprint, jsonify, request, abort
from ..util.decorators import require_api_key
from ..models import User
from ..schemas import user_schema
from ..default_settings import *
from datetime import datetime
from ..application import db


website_api = Blueprint('website_api', __name__, url_prefix='/website/api/v1')


def build_message(success, status_code, message):
    return jsonify({'success': success, 'status_code': status_code, 'message': message})


class BaseObjectAPI(object):
    def __init__(self, data_as_json):
        self.errors = []
        self.data_as_json = data_as_json

    def validate_required_fields(self, field):
        if not self.data_as_json.get(field):
            self.errors.append('{} field is required'.format(field))

    def get_message_errors(self):
        message = []
        for e in self.errors:
            message.append(e)
        return message


class UserAPI(BaseObjectAPI):
    def user_check_unique(self, field):
        if field == 'email':
            r_query = User.query.filter_by(user_email=self.data_as_json.get('user_email'))

        internal = self.data_as_json.get('internal')
        if internal:
            r_query = r_query.filter(User.internal != internal)

        if r_query.first():
            self.errors.append(u'E-mail informado já encontra-se cadastrado.')


@website_api.errorhandler(500)
def internal_server_error(e):
    response = build_message(success=False, status_code=500, message='internal server error')
    return response, 500


@website_api.route('/users', methods=['GET'])
@require_api_key
def get_users():
    users = User.query.all()
    r_users = user_schema.dump(users, many=True)
    return jsonify(r_users.data)


@website_api.route('/users', methods=['POST'])
def persist_user():
    backdoor_key = request.headers.get('xf-backdoor-access-key')

    if not request.content_type.startswith('application/json'):
        return build_message(success=False, status_code=500, message='content-type not supported'), 500

    if backdoor_key and backdoor_key == BACKDOOR_ACCESS_KEY:
        data_as_json = request.get_json(silent=True)

        user_api = UserAPI(data_as_json)
        user_api.validate_required_fields('name')
        user_api.validate_required_fields('user_email')
        user_api.validate_required_fields('user_password')
        user_api.user_check_unique(field='email')

        if user_api.errors:
            return build_message(success=False, status_code=400, message=user_api.get_message_errors()), 400

        user = User.from_dict(data_as_json)

        if not user.internal:
            user.internal = uuid.uuid4()
        if not user.created:
            user.created = datetime.now()

        try:
            db.session.add(user)
            db.session.commit()

            response = build_message(success=True, status_code=201, message='persisted')
            return response
        except Exception as e:
            abort(500, e)

    return build_message(success=False, status_code=404, message='not found')
