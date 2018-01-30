import uuid

from flask import Blueprint, jsonify, request, abort
from ..util.decorators import require_api_key
from ..models import User
from ..schemas import user_schema

website_api = Blueprint('website_api', __name__, url_prefix='/website/api/v1')


@website_api.errorhandler(500)
def internal_server_error(e):
    response = jsonify({'success': False, 'message': 'internal server error'})
    return response, 500


@website_api.route('/users', methods=['GET'])
@require_api_key
def get_social_networks():
    users = User.query.all()
    r_users = user_schema.dump(users, many=True)
    return jsonify(r_users.data)

