from flask import request
from flask_restful import Resource
from aylienapiclient import textapi

from secrets_apis import AYLIEN_APP_ID, AYLIEN_API_KEY
from controllers.jwt_validator import validate_jwt
from db.user import users


class EntityExtraction(Resource):
    def post(self):
        data = request.get_json()
        decoded = None
        secret_token = request.headers['Authorization']

        try:
            decoded = validate_jwt(secret_token)
        except:
            return {'error': True, 'errorMessage': 'Invalid secret token'}, 403

        if not decoded:
            return {'error': True, 'errorMessage': 'Invalid secret token'}, 403

        db_data = users.find_one({'email': decoded['email']})

        flag = 0
        for app in db_data['applications']:
            if app['name'] == decoded['app_name'] and app['secret_token'] == secret_token and 'entities' in app['allowed_apis']:
                flag = 1

        if flag == 0:
            return {'error': True, 'errorMessage': 'Invalid secret token'}, 403

        client = textapi.Client(AYLIEN_APP_ID, AYLIEN_API_KEY)
        entities = client.Entities({'text': data['text']})

        return {'error': False, 'results': entities}
