from flask import request
from flask_restful import Resource
from aylienapiclient import textapi

from secrets_apis import AYLIEN_APP_ID, AYLIEN_API_KEY
from controllers.jwt_validator import validate_jwt


class Summarizer(Resource):
    def post(self):
        data = request.get_json()
        is_valid = None
        try:
            is_valid = validate_jwt(request.headers['Authorization'])
        except:
            return {'error': True, 'errorMessage': 'Invalid access_token'}, 400

        if not is_valid:
            return {'error': True, 'errorMessage': 'Invalid access_token'}, 400

        client = textapi.Client(AYLIEN_APP_ID, AYLIEN_API_KEY)
        summary = client.Summarize(
            {'text': data['text'], 'title': data['title'], 'sentences_number': 3})

        return {'error': False, 'results': summary}
