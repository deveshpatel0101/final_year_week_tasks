from flask import request
from flask_restful import Resource
from pymongo import ReturnDocument
import jwt
import uuid
import os

from app.db.user import users
from app.controllers.jwt_validator import validate_jwt
from app.validators.project import create_project_validator, delete_project_validator, update_project_validator
from app.controllers.time import current_sec_time


class Project(Resource):
    def post(self):
        decoded = None
        try:
            decoded = validate_jwt(request.headers['Authorization'])
        except:
            return {'error': True, 'errorType': 'access_token', 'errorMessage': 'Invalid access_token.'}, 400

        if not decoded:
            return {'error': True, 'errorType': 'access_token', 'errorMessage': 'Invalid access_token.'}, 400

        data = request.get_json()
        data['requests'] = {'entities': [], 'translator': [],
                            'summarizer': [], 'sentiment': []}

        isValid = create_project_validator.validate({'data': data})
        errors = create_project_validator.errors

        if not isValid:
            errors = errors['data'][0]

        if 'name' in errors:
            return {'error': True, 'errorType': 'name', 'errorMessage': errors['name'][0]}, 400
        elif 'allowed_apis' in errors:
            return {'error': True, 'errorType': 'allowed_apis', 'errorMessage': errors['allowed_apis'][0]}, 400

        db_data = users.find_one({'rid': decoded['rid']})

        if db_data['account_type'] == 'free' and len(db_data['applications']) == 3:
            return {'error': True, 'errorType': 'applications', 'errorMessage': 'You have reached maximum limit of applications you can create. Subscribe to premium and create unlimited applications.'}, 400

        for app in db_data['applications']:
            if app['name'] == data['name']:
                return {'error': True, 'errorType': 'name', 'errorMessage': 'Application with the similar name already exist.'}, 400

        payload = {'rid': db_data['rid'], 'id': str(uuid.uuid4())}

        data['secret_token'] = jwt.encode(
            payload,
            os.getenv('JWT_SECRET'), algorithm='HS256').decode()

        data['created_at'] = current_sec_time()

        results = users.find_one_and_update({'email': db_data['email']}, {
            '$push': {'applications': data}}, return_document=ReturnDocument.AFTER)

        if not results:
            print(results)
            return {'error': True, 'errorType': 'server', 'errorMessage': 'Something went wrong from our side. Sorry for the incovenience.'}, 500

        for app in results['applications']:
            del app['requests']
            del app['secret_token']

        del data['secret_token']
        del data['requests']

        return {'error': False, 'results': results['applications'], 'added': data}, 200

    def get(self):
        decoded = None
        try:
            decoded = validate_jwt(request.headers['Authorization'])
        except:
            return {'error': True, 'errorType': 'access_token', 'errorMessage': 'Invalid access_token.'}, 400

        if not decoded:
            return {'error': True, 'errorType': 'access_token', 'errorMessage': 'Invalid access_token.'}, 400

        data = users.find_one({'rid': decoded['rid']})

        if not data:
            return {'error': True, 'errorType': 'server', 'errorMessage': 'Something went wrong from our side. Sorry for the incovenience.'}, 500

        for app in data['applications']:
            del app['secret_token']
            del app['requests']

        return {'error': False, 'results': {'projects': data['applications']}}, 200

    def delete(self):
        decoded = None
        try:
            decoded = validate_jwt(request.headers['Authorization'])
        except:
            return {'error': True, 'errorType': 'access_token', 'errorMessage': 'Invalid access_token.'}, 400

        if not decoded:
            return {'error': True, 'errorType': 'access_token', 'errorMessage': 'Invalid access_token.'}, 400

        data = request.get_json()

        delete_project_validator.validate(data)
        errors = delete_project_validator.errors

        if errors and 'name' in errors:
            return {'error': True, 'errorType': 'name', 'errorMessage': errors['name'][0]}, 400

        db_data = users.find_one({'rid': decoded['rid']})

        if not db_data:
            return {'error': True, 'errorType': 'server', 'errorMessage': 'Something went wrong from our side. Sorry for the incovenience.'}, 500

        deleted = {}
        for app in db_data['applications']:
            if app['name'] == data['name']:
                deleted = app

                updated = users.find_one_and_update({'rid': decoded['rid']}, {
                    '$pull': {'applications': {'name': data['name']}}}, return_document=ReturnDocument.AFTER)

                for update in updated['applications']:
                    del update['secret_token']
                    del update['requests']

                del deleted['secret_token']
                del deleted['requests']

                return {'error': False, 'deleted': deleted, 'results': {'projects': updated['applications']}}

        return {'error': True, 'errorType': 'name', 'errorMessage': 'Application not found under the specified name.'}, 400

    def put(self):
        decoded = None
        try:
            decoded = validate_jwt(request.headers['Authorization'])
        except:
            return {'error': True, 'errorType': 'access_token', 'errorMessage': 'Invalid access_token.'}, 400

        if not decoded:
            return {'error': True, 'errorType': 'access_token', 'errorMessage': 'Invalid access_token.'}, 400

        data = request.get_json()

        update_project_validator.validate(data)
        errors = update_project_validator.errors

        if 'name' in errors:
            return {'error': True, 'errorType': 'name', 'errorMessage': errors['name'][0]}, 400
        elif 'update' in errors:
            return {'error': True, 'errorType': 'update', 'errorMessage': errors['update'][0]}, 400
        elif 'name' not in data['update'] and 'allowed_apis' not in data['update']:
            return {'error': True, 'errorType': 'no update', 'errorMessage': 'No fields specified to update.'}, 400

        db_data = users.find_one({'rid': decoded['rid']})

        if not db_data:
            return {'error': True, 'errorType': 'server', 'errorMessage': 'Something went wrong from our side. Sorry for the incovenience.'}, 500

        before_update = None
        for app in db_data['applications']:
            if app['name'] == data['name']:
                before_update = app

        if not before_update:
            return {'error': True, 'errorType': 'name',
                    'errorMessage': 'Application not found under the specified name.'}, 400

        if 'name' in data['update']:
            for app in db_data['applications']:
                if app['name'] == data['update']['name']:
                    return {'error': True, 'errorType': 'update.name', 'errorMessage': 'Application with the similar name already exist.'}, 400
        elif 'allowed_apis' in data['update'] and db_data['account_type'] == 'free' and len(data['update']['allowed_apis']) > 2:
            return {'error': True, 'errorType': 'allowed_apis', 'errorMessage': 'Free acount tier user can select only two apis per project.'}, 400
    
        after_update = None

        if 'name' in data['update'] and 'allowed_apis' in data['update']:
            after_update = users.find_one_and_update({'rid': decoded['rid'], 'applications.name': data['name']}, {'$set': {
                'applications.$.name': data['update']['name'], 'applications.$.allowed_apis': data['update']['allowed_apis']}}, return_document=ReturnDocument.AFTER)
        elif 'name' in data['update']:
            after_update = users.find_one_and_update({'rid': decoded['rid'], 'applications.name': data['name']}, {'$set': {
                'applications.$.name': data['update']['name']}}, return_document=ReturnDocument.AFTER)
        elif 'allowed_apis' in data['update']:
            after_update = users.find_one_and_update({'rid': decoded['rid'], 'applications.name': data['name']}, {'$set': {
                'applications.$.allowed_apis': data['update']['allowed_apis']}}, return_document=ReturnDocument.AFTER)

        if not after_update:
            return {'error': True, 'errorType': 'name',
                    'errorMessage': 'Application not found under the specified name.'}, 400

        for app in after_update['applications']:
            del app['secret_token']
            del app['requests']

        del before_update['secret_token']
        del before_update['requests']

        return {'error': False, 'updated': before_update, 'results': {'projects': after_update['applications']}}
