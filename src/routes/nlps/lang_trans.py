from flask import request
from flask_restful import Resource
from controllers.jwt_validator import validate_jwt


class Translate(Resource):
    def post(self):
        data = request.get_json()
        is_valid = validate_jwt(request.headers['Authorization'])
        if not is_valid:
            return {'error': True, 'errorMessage': 'Invalid access_token'}, 400

        return {'error': False, 'data': data, 'is_valid': is_valid}
