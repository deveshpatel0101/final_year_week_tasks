from flask import request
from flask_restful import Resource
from pymongo import ReturnDocument
import jwt

from db.user import users
from controllers.jwt_validator import validate_jwt
from validators.create_app import create_app_validator
from secrets_apis import JWT_SECRET


class CreateApp(Resource):
    def post(self):
        decoded = None
        try:
            decoded = validate_jwt(request.headers['Authorization'])
        except:
            return {'error': True, 'errorMessage': 'Invalid access_token'}, 400

        if not decoded:
            return {'error': True, 'errorMessage': 'Invalid access_token'}, 400

        data = request.get_json()

        if not create_app_validator.validate({'data': data}):
            return {'error': True, 'errorMessage': create_app_validator.errors['data'][0]}, 400

        db_data = users.find_one({'email': decoded['email']})

        for app in db_data['applications']:
            if app['name'] == data['name']:
                return {'error': True, 'errorMessage': {'name': ['Application with the similar name already exist.']}}

        data['secret_token'] = jwt.encode(
            {'email': db_data['email'],
             'allowed_apis': data['allowed_apis'],
             'app_name': data['name']
             },
            JWT_SECRET, algorithm='HS256').decode()

        results = users.find_one_and_update({'email': db_data['email']}, {
            '$push': {'applications': data}}, return_document=ReturnDocument.AFTER)

        if not results:
            print(results)
            return {'error': True, 'errorMessage': 'Something went wrong from our side. Sorry for the incovenience.'}, 500

        return {'error': False, 'results': results['applications'], 'updated': data}, 200
