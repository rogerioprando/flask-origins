import uuid

from flask import Blueprint, jsonify, request, abort
from ..util.decorators import require_api_key
from ..models import User
from ..schemas import user_schema
from ..default_settings import *
from datetime import datetime
from ..application import db
from ..integrations import build_message, UserAPI


website_api = Blueprint('website_api', __name__, url_prefix='/website/api/v1')


@website_api.errorhandler(401)
def unauthorized_error(e):
    response = build_message(success=False, status_code=401, message='request unauthorized')
    return response, 401


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
    """
    payload for persistence

    {
        "active": true,
        "company": "Linux Foundation",
        "created": "2018-01-30T11:33:03.309602+00:00",
        "is_admin": false,
        "occupation": "Sr Software Engineer",
        "name": "Alan Cox",
        "user_email": "alan.cox@linux.org",
        "user_password": "123"
    }

    """

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
