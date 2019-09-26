from flask import request
from flask_restful import Resource
from pymongo import ReturnDocument
import jwt
import uuid
import os

from app.db.user import users
from app.controllers.jwt_validator import validate_jwt
from app.validators.create_app import create_app_validator
from app.controllers.time import current_sec_time


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
        data['requests'] = []

        if not create_app_validator.validate({'data': data}):
            return {'error': True, 'errorMessage': create_app_validator.errors['data'][0]}, 400

        db_data = users.find_one({'rid': decoded['rid']})

        if db_data['account_type'] == 'free' and len(db_data['applications']) == 3:
            return {'error': True, 'errorMessage': {'applications': ['You have reached maximum limit of applications you can create. Subscribe to premium and create unlimited applications.']}}

        for app in db_data['applications']:
            if app['name'] == data['name']:
                return {'error': True, 'errorMessage': {'name': ['Application with the similar name already exist.']}}

        payload = {'rid': db_data['rid'], 'id': str(uuid.uuid4())}

        data['secret_token'] = jwt.encode(
            payload,
            os.getenv('JWT_SECRET'), algorithm='HS256').decode()

        data['created_at'] = current_sec_time()

        results = users.find_one_and_update({'email': db_data['email']}, {
            '$push': {'applications': data}}, return_document=ReturnDocument.AFTER)

        if not results:
            print(results)
            return {'error': True, 'errorMessage': 'Something went wrong from our side. Sorry for the incovenience.'}, 500

        for app in results['applications']:
            del app['requests']
            del app['secret_token']

        del data['secret_token']
        del data['requests']

        return {'error': False, 'results': results['applications'], 'added': data}, 200
