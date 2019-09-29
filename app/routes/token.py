from flask import request
from flask_restful import Resource

from app.controllers.jwt_validator import validate_jwt
from app.db.user import users


class Token(Resource):
    def get(self):
        decoded = None
        access_token = request.headers['Authorization']
        app_name = request.args['name']

        try:
            decoded = validate_jwt(access_token)
        except:
            return {'error': True, 'errorType': 'secret_token', 'errorMessage': 'Invalid secret token'}, 403

        if not decoded:
            return {'error': True, 'errorType': 'secret_token', 'errorMessage': 'Invalid secret token'}, 403

        if not app_name:
            return {'error': True, 'errorType': 'name', 'errorMessage': 'Parameter \'name\' not found.'}, 400

        db_data = users.find_one({'rid': decoded['rid']})

        if not db_data:
            return {'error': True, 'errorType': 'server', 'errorMessage': 'Something went wrong from our side. Sorry for the incovenience.'}, 500

        for app in db_data['applications']:
            if app['name'] == app_name:
                return {'error': False, 'secret_token': app['secret_token']}

        return {'error': True, 'errorType': 'application', 'errorMessage': 'Application not found under the specified name.'}
