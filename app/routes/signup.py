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


        signup_validator.validate(data)
        errors = signup_validator.errors

        if 'fname' in errors:
            return {'error': True, 'errorType': 'fname', 'errorMessage': errors['fname'][0]}, 400
        elif 'lname' in errors:
            return {'error': True, 'errorType': 'lname', 'errorMessage': errors['lname'][0]}, 400
        elif 'email' in errors:
            return {'error': True, 'errorType': 'email', 'errorMessage': errors['email'][0]}, 400
        elif 'password' in errors:
            return {'error': True, 'errorType': 'password', 'errorMessage': 'Password should contain: 6 characters or more, 1 uppercase letter and 1 special or numeric character.'}, 400
        elif 'cpassword' in errors:
            return {'error': True, 'errorType': 'cpassword', 'errorMessage': 'Password should contain: 6 characters or more, 1 uppercase letter and 1 special or numeric character.'}, 400
        elif data['cpassword'] != data['password']:
            return {'error': True, 'errorType': 'cpassword', 'errorMessage': 'Both passwords should match.'}

        del data['cpassword']

        result = users.find_one({'email': data['email']})

        if result:
            return {'error': True, 'errorType': 'email', 'errorMessage': 'User already exists!'}, 400

        data['password'] = bcrypt.hashpw(
            data['password'].encode(), bcrypt.gensalt()).decode()

        data['rid'] = str(uuid.uuid4())

        result = users.save(data)

        if not result:
            return {'error': True, 'errorType': 'server', 'errorMessage': 'Something went wrong from our side. Sorry for the incovenience.'}, 500

        return {'error': False, 'results': 'Signup successful!'}, 200
