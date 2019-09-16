import jwt
import os
from app.controllers.time import current_sec_time


def validate_jwt(token):
    try:
        if token:
            decoded = jwt.decode(token.encode(), os.getenv(
                'JWT_SECRET'), algorithms=['HS256'])
    except:
        return False
    return decoded
