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

        signin_validator.validate(data)
        errors = signin_validator.errors

        if 'email' in errors:
            return {'error': True, 'errorType': 'email', 'errorMessage': errors['email'][0]}, 400
        elif 'password' in errors:
            return {'error': True, 'errorType': 'password', 'errorMessage': 'Password should contain: 6 characters or more, 1 uppercase letter and 1 special or numeric character.'}, 400

        result = users.find_one({'email': data['email']})

        if not result:
            return {'error': True, 'errorType': 'email', 'errorMessage': 'Invalid email.'}, 400

        pwd = bcrypt.checkpw(data['password'].encode(),
                             result['password'].encode())

        if not pwd:
            return {'error': True, 'errorType': 'password', 'errorMessage': 'Incorrect password'}, 400

        curr_time = current_sec_time()

        payload = {'rid': str(result['rid']),
                   'id': str(uuid.uuid4()),
                   'iat': curr_time,
                   'exp': curr_time + 86400
                   }

        encoded_jwt = jwt.encode(
            payload,
            os.getenv('JWT_SECRET'), algorithm='HS256')

        return {'error': False,
                'access_token': encoded_jwt.decode(),
                'userDate': {'fname': result['fname'],
                             'lname': result['lname'],
                             'accountType': result['account_type']
                             }
                }
