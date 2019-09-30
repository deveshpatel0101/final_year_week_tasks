from flask import request
from flask_restful import Resource

from app.controllers.jwt_validator import validate_jwt
from app.db.user import users
from app.db.redis import rds, rds_for_db


class Usage(Resource):
    def get(self):
        decoded = None
        access_token = request.headers['Authorization']
        app_name = request.args['name']

        try:
            decoded = validate_jwt(access_token)
        except:
            return {'error': True, 'errorType': 'secret_token', 'errorMessage': 'Invalid secret token'}, 403

        if not decoded:
            return {'error': True, 'errorType': 'secret_token', 'errorMessage': 'Invalid secret token'}, 403

        if not app_name:
            return {'error': True, 'errorType': 'name', 'errorMessage': 'Application name not specified in the parameter.'}

        db_data = users.find_one({'rid': decoded['rid']})

        if not db_data:
            return {'error': True, 'errorType': 'server', 'errorMessage': 'Something went wrong from our side. Sorry for the incovenience.'}, 500

        for app in db_data['applications']:
            if app_name == app['name']:
                for allowed_api in app['allowed_apis']:
                    rid = db_data['rid']
                    search = f'{rid}:{allowed_api}'
                    rds_data = rds.lrange(search, 0, -1)
                    in_update_data = rds_for_db.lrange(search, 0, -1)

                    if in_update_data:
                        app['isInUpdate'] = True

                    rds_data = rds_data + in_update_data

                    for i in range(len(rds_data)):
                        rds_data[i] = rds_data[i].decode()

                    app['requests'][allowed_api] = app['requests'][allowed_api] + rds_data

                del app['secret_token']
                return {'error': False, 'results': {'usage': app['requests']}}

        return {'error': True, 'errorType': 'name', 'errorMessage': 'Application not found under the specified name.'}
