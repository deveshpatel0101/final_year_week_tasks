from flask import request
from flask_restful import Resource
import bcrypt

from db.user import users
from validators.signup import signup_validator


class SignUp(Resource):
    def post(self):
        data = request.get_json()
        if not signup_validator.validate(data) or data['password'] != data['cpassword']:
            errors = signup_validator.errors
            if data['password'] != data['cpassword']:
                errors['cpassword'] = ['Both passwords should match.']
            return {'error': True, 'errorMesssage': errors}, 400

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
