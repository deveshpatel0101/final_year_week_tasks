from flask import request
from flask_restful import Resource
from aylienapiclient import textapi
import os

from app.controllers.jwt_validator import validate_jwt
from app.validators.nlps.entities import entities_validator
from app.db.user import users
from app.controllers.redis_ops import increment, isAllowed, getAll


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

        if not entities_validator.validate(data):
            return {'error': True, 'errorMessage': entities_validator.errors}, 400

        db_data = users.find_one({'rid': decoded['rid']})

        flag = 0
        for app in db_data['applications']:
            if app['secret_token'] == secret_token and 'entities' in app['allowed_apis']:
                flag = 1

        if flag == 0:
            return {'error': True, 'errorMessage': 'Invalid secret token'}, 403

        increment(decoded['rid'], 'entities')

        if not isAllowed(decoded['rid'], db_data['account_type']):
            return {'error': True, 'errorMessage': 'Your per day usage quota has exceeded.'}, 400

        client = textapi.Client(
            os.getenv('AYLIEN_APP_ID'), os.getenv('AYLIEN_API_KEY'))
        entities = client.Entities({'text': data['text']})

        return {'error': False, 'results': entities}
