from flask import request
from flask_restful import Resource
import bcrypt
import jwt
import uuid
import os

from app.db.user import users
from app.validators.signin import signin_validator
from app.controllers.time import current_sec_time


class SignIn(Resource):
    def post(self):
        data = request.get_json()

        if not signin_validator.validate(data):
            return {'error': True, 'errorMessage': signin_validator.errors}, 400

        result = users.find_one({'email': data['email']})

        if not result:
            return {'error': True, 'errorMessage': 'User does not exist!'}, 400

        pwd = bcrypt.checkpw(data['password'].encode(),
                             result['password'].encode())

        if not pwd:
            return {'error': True, 'errorMessage': 'Invalid password'}, 400

        curr_time = current_sec_time()

        payload = {'rid': str(result['rid']),
                   'id': str(uuid.uuid4()),
                   'iat': curr_time,
                   'exp': curr_time + 86400
                   }

        encoded_jwt = jwt.encode(
            payload,
            os.getenv('JWT_SECRET'), algorithm='HS256')

        return {'error': False, 'access_token': encoded_jwt.decode()}
