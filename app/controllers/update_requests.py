from app.db.user import users
from app.db.redis import rds_for_db
from app.controllers.jwt_validator import validate_jwt


def push_requests_to_db():
    keys = rds_for_db.keys('*')
    for key in keys:
        requests = rds_for_db.lrange(key, 0, -1)
        for i in range(len(requests)):
            requests[i] = requests[i].decode()

        key, api_type = key.decode().split(':')
        decoded = validate_jwt(key)
        db_data = users.find_one({'email': decoded['email']})
        for app in db_data['applications']:
            if app['secret_token'] == key:
                app['requests'] = app['requests'] + requests
                users.find_one_and_update({'email': decoded['email']}, {
                                          '$set': {'applications': db_data['applications']}})
                to_delete = f'{key}:{api_type}'
                rds_for_db.delete(to_delete)
                break
