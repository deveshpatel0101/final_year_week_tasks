from flask import request
from flask_restful import Resource
import bcrypt

from db.user import users
from validators.signup import signup_validator


class SignUp(Resource):
    def post(self):
        data = request.get_json()
        if not signup_validator.validate(data):
            print(signup_validator.errors)
            return {'error': True, 'errorMesssage': signup_validator.errors}, 400

        if data['password'] != data['cpassword']:
            return {'error': True, 'errorMessage': {'cpassword': ['Both passwords should match']}}, 400

        del data['cpassword']

        result = users.find_one({'email': data['email']})

        if result:
            return {'error': True, 'errorMessage': 'User already exists!'}, 400

        data['password'] = bcrypt.hashpw(
            data['password'].encode(), bcrypt.gensalt()).decode()

        result = users.save(data)

        if result:
            return {'error': False, 'errorMessage': 'Signup successful!'}, 200

        return {'error': True, 'errorMessage': 'Something went wrong from our side. Sorry for the incovenience.'}, 500
