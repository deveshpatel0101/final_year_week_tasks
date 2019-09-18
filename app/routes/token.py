from flask import request
from flask_restful import Resource

from app.controllers.jwt_validator import validate_jwt
from app.db.user import users


class Token(Resource):
    def get(self):
        decoded = None
        access_token = request.headers['Authorization']
        app_name = request.args['name']

        print(app_name)

        try:
            decoded = validate_jwt(access_token)
        except:
            return {'error': True, 'errorMessage': 'Invalid secret token'}, 403

        if not decoded:
            return {'error': True, 'errorMessage': 'Invalid secret token'}, 403

        if not app_name:
            return {'error': True, 'errorMessage': {'name': ['Parameter name required.']}}, 400

        db_data = users.find_one({'email': decoded['email']})

        if not db_data:
            return {'error': True, 'errorMessage': 'Something went wrong from our side. Sorry for the incovenience.'}, 500

        for app in db_data['applications']:
            if app['name'] == app_name:
                return {'error': False, 'results': {'secret_token': app['secret_token']}}

        return {'error': True, 'errorMessage': {'applications': ['Application not found under the specified name.']}}
