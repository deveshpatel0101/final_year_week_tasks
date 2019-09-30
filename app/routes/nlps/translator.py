from flask import request
from flask_restful import Resource
import requests
import os

from app.controllers.jwt_validator import validate_jwt
from app.validators.nlps.translator import translator_validator
from app.controllers.redis_ops import increment, isAllowed
from app.db.user import users


class Translate(Resource):
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

        if not translator_validator.validate(data):
            return {'error': True, 'errorMessage': translator_validator.errors}, 400

        db_data = users.find_one({'rid': decoded['rid']})

        flag = 0
        for app in db_data['applications']:
            if app['secret_token'] == secret_token and 'translator' in app['allowed_apis']:
                flag = 1

        if flag == 0:
            return {'error': True, 'errorMessage': 'Invalid secret token'}, 403

        increment(decoded['rid'], 'translator')

        if not isAllowed(decoded['rid'], db_data['account_type'], 'translator', secret_token):
            return {'error': True, 'errorMessage': 'Your per day usage quota has exceeded.'}, 400

        lang = data['lang']
        text = data['text']

        YANDEX_TRANSLATE_API_KEY = os.getenv('YANDEX_TRANSLATE_API_KEY')

        r = requests.get(
            f'https://translate.yandex.net/api/v1.5/tr.json/translate?key={YANDEX_TRANSLATE_API_KEY}&text={text}&lang={lang}&options=1')

        r_data = r.json()
        del r_data['code']

        return {'error': False, 'results': r_data}
