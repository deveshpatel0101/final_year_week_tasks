from cerberus import Validator

signin_schema = {
    'email': {
        'type': 'string',
        'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
        'required': True
    },
    'password': {
        'type': 'string',
        'regex': '^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).{4,}$',
        'required': True
    }
}

signin_validator = Validator(signin_schema)
