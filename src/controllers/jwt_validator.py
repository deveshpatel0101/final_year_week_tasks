import jwt
from controllers.time import current_sec_time


def validate_jwt(token):
    try:
      if token:
        token = token.split(' ')[1]
        decoded = jwt.decode(token.encode(), 'some long secret', algorithms=['HS256'])
    except:
      return False
    return True
