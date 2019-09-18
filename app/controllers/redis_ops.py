from threading import Thread

from app.db.redis import rds
from app.controllers.time import current_sec_time
from app.controllers.update_requests import push_requests_to_db
from app.db.redis import rds_for_db

def isAllowed(key, account_type):
    allowed = f'{key}:allowed'
    count = f'{key}:count'
    if rds.get(allowed) == 'False' or (int(rds.get(count).decode()) > 100 and account_type == 'free'):
        rds.rpop(key)
        rds.decr(count)
        return False
    return True


def increment(key, api_type):
    count = f'{key}:count'
    first_call = f'{key}:first_call'
    allowed = f'{key}:allowed'
    main_key = f'{key}:{api_type}'

    if rds.lrange(main_key, 0, -1):
        rds.rpush(main_key, current_sec_time())
        rds.incr(count)

        if rds.llen(main_key) > 100 and not rds_for_db.lrange(main_key, 0, -1):
            rds.move(main_key, 1)
            rds.set(allowed, 'False')
            t1 = Thread(target=push_requests_to_db)
            t1.start()
        return True

    rds.rpush(main_key, current_sec_time())
    rds.set(count, 1)
    rds.set(first_call, current_sec_time())
    rds.set(allowed, 'True')
    return True


def getAll(key, api_type):
    count = f'{key}:count'
    first_call = f'{key}:first_call'
    main_key = f'{key}:{api_type}'
    data = {}

    data['allowed'] = isAllowed(main_key)
    data['count'] = rds.get(count)
    data['calls'] = rds.lrange(main_key, 0, -1)
    data['first_call'] = rds.get(first_call)

    return data
