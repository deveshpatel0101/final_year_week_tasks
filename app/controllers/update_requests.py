from pymongo import ReturnDocument

from app.db.user import users
from app.db.redis import rds_for_db
from app.controllers.jwt_validator import validate_jwt


def push_requests_to_db(requests, main_key):
    for i in range(len(requests)):
        requests[i] = requests[i].decode()

    key, api_type = main_key.split(':')
    decoded = validate_jwt(key)
    db_data = users.find_one({'rid': decoded['rid']})
    if db_data:
        for app in db_data['applications']:
            if app['secret_token'] == key:
                app['requests'] = app['requests'] + requests
                updated = users.find_one_and_update({'rid': decoded['rid']}, {
                    '$set': {'applications': db_data['applications']}}, return_document=ReturnDocument.AFTER)
                if not updated:
                    rds_for_db.rpush(main_key, *requests)
                break
