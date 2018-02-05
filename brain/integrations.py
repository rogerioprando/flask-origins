from flask import jsonify
from .models import User


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
