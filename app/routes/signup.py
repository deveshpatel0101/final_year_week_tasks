from flask import request
from flask_restful import Resource
import bcrypt
import uuid

from app.db.user import users
from app.validators.signup import signup_validator


class SignUp(Resource):
    def post(self):
        data = request.get_json()
        data['account_type'] = 'free'
        data['applications'] = []

        if (not signup_validator.validate(data)) or (not 'password' in data) or (not 'cpassword' in data) or (data['password'] != data['cpassword']):
            errors = signup_validator.errors
            if (('password' in data) and ('cpassword' in data)) and data['password'] != data['cpassword']:
                errors['cpassword'] = ['Both passwords should match.']
            return {'error': True, 'errorMesssage': errors}, 400

        del data['cpassword']

        result = users.find_one({'email': data['email']})

        if result:
            return {'error': True, 'errorMessage': 'User already exists!'}, 400

        data['password'] = bcrypt.hashpw(
            data['password'].encode(), bcrypt.gensalt()).decode()

        data['rid'] = str(uuid.uuid4())

        result = users.save(data)

        if not result:
            return {'error': True, 'errorMessage': 'Something went wrong from our side. Sorry for the incovenience.'}, 500

        return {'error': False, 'results': 'Signup successful!'}, 200
