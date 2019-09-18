from flask import request
from flask_restful import Resource

from app.controllers.jwt_validator import validate_jwt
from app.db.user import users
from app.db.redis import rds, rds_for_db


class Usage(Resource):
    def get(self):
        decoded = None
        access_token = request.headers['Authorization']

        try:
            decoded = validate_jwt(access_token)
        except:
            return {'error': True, 'errorMessage': 'Invalid secret token'}, 403

        if not decoded:
            return {'error': True, 'errorMessage': 'Invalid secret token'}, 403

        db_data = users.find_one({'email': decoded['email']})

        if not db_data:
            return {'error': True, 'errorMessage': 'Something went wrong from our side. Sorry for the incovenience.'}, 500

        for app in db_data['applications']:
            for allowed_api in app['allowed_apis']:
                secret_token = app['secret_token']
                search = f'{secret_token}:{allowed_api}'
                rds_data = rds.lrange(search, 0, -1)
                in_update_data = rds_for_db.lrange(search, 0, -1)

                if in_update_data:
                    app['isInUpdate'] = True

                rds_data = rds_data + in_update_data

                for i in range(len(rds_data)):
                    rds_data[i] = rds_data[i].decode()

                app['requests'] = app['requests'] + rds_data

        for app in db_data['applications']:
            del app['secret_token']

        return {'error': False, 'results': {'applications': db_data['applications']}}
