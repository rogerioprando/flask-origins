from .application import ma


class UserSchema(ma.Schema):
    class Meta:
        fields = ('internal', 'created', 'active', 'name', 'user_name',
                  'user_email', 'is_admin', 'company', 'occupation')

user_schema = UserSchema()
