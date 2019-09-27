from threading import Thread
import datetime

from app.db.redis import rds
from app.controllers.time import current_sec_time
from app.controllers.update_requests import push_requests_to_db
from app.db.redis import rds_for_db


def isAllowed(key, account_type, api_type):
    main_key = f'{key}:{api_type}'

    # if premium account allow unlimited calls
    if account_type == 'premium':
        start_new_thread(key, api_type)
        return True

    # get all and decode the dict
    data = rds.hgetall(key)
    data = {y.decode('ascii'): data.get(y).decode('ascii')
            for y in data.keys()}

    # if allowed is false
    if data['allowed'] == 'False' or int(data['count']) > 100:
        first_access = datetime.datetime.fromtimestamp(
            data['first_call']).strftime('%d-%B-%Y')
        today = (datetime.datetime.now()).strftime('%d-%B-%Y')

        # check if request is on new day
        if first_access != today:
            new_data = {'count': 1, 'allowed': 'True',
                        'first_call': current_sec_time()}
            rds.hmset(key, new_data)
            start_new_thread(key, api_type)
            return True

        # pop one request and increment count by -1
        rds.rpop(main_key)
        rds.hincrby(key, 'count', -1)
        rds.hset(key, 'allowed', 'False')
        start_new_thread(key, api_type)

        return False

    first_access = datetime.datetime.fromtimestamp(
        data['first_call']).strftime('%d-%B-%Y')
    today = (datetime.datetime.now()).strftime('%d-%B-%Y')

    # check if request is on new day
    if first_access != today:
        new_data = {'count': 1, 'allowed': 'True',
                    'first_call': current_sec_time()}
    start_new_thread(key, api_type)

    return True


def increment(key, api_type):
    main_key = f'{key}:{api_type}'

    data = rds.hgetall(key)
    data = {y.decode('ascii'): data.get(y).decode('ascii')
            for y in data.keys()}

    if data:
        rds.rpush(main_key, current_sec_time())
        rds.hincrby(key, 'count', 1)
        return True

    new_data = {'count': 1, 'first_call': current_sec_time(),
                'allowed': 'True'}
    rds.rpush(main_key, current_sec_time())
    rds.hmset(key, new_data)
    return True


def start_new_thread(key, api_type):
    main_key = f'{key}:{api_type}'

    if rds.llen(main_key) > 100 and not rds_for_db.lrange(main_key, 0, -1):
        check = rds.move(main_key, 1)
        if check:
            t1 = Thread(target=push_requests_to_db)
            t1.start()

    return
