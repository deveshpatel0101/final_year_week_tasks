from flask import request
from flask_restful import Resource
from aylienapiclient import textapi
import os

from app.controllers.jwt_validator import validate_jwt
from app.validators.nlps.sentiment import sentiment_validator
from app.db.user import users


class Sentiment(Resource):
    def post(self):
        data = request.get_json()
        decoded = None
        secret_token = request.headers['Authorization']

        try:
            decoded = validate_jwt(secret_token)
        except:
            return {'error': True, 'errorMessage': 'Invalid access_token'}, 403

        if not decoded:
            return {'error': True, 'errorMessage': 'Invalid access_token'}, 403

        if not sentiment_validator.validate(data):
            return {'error': True, 'errorMessage': sentiment_validator.errors}, 400

        db_data = users.find_one({'email': decoded['email']})

        flag = 0
        for app in db_data['applications']:
            if app['name'] == decoded['app_name'] and app['secret_token'] == secret_token and 'sentiment' in app['allowed_apis']:
                flag = 1

        if flag == 0:
            return {'error': True, 'errorMessage': 'Invalid secret token'}, 403

        client = textapi.Client(
            os.getenv('AYLIEN_APP_ID'), os.getenv('AYLIEN_API_KEY'))
        sentiment = client.Sentiment({'text': data['text']})

        return {'error': False, 'results': sentiment}