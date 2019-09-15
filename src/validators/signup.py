from cerberus import Validator

signup_schema = {
    'email': {
        'type': 'string',
        'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
        'required': True
    },
    'fname': {
        'type': 'string',
        'minlength': 3,
        'required': True
    },
    'lname': {
        'type': 'string',
        'minlength': 3,
        'required': True
    },
    'password': {
        'type': 'string',
        'regex': '^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).{4,}$',
        'required': True
    },
    'cpassword': {
        'type': 'string',
        'regex': '^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).{4,}$',
        'required': True
    },
    'account_type': {
        'type': 'string',
        'regex': '^(free)$',
        'required': True
    },
    'applications': {
        'type': 'list',
        'maxlength': 0,
        'required': True
    }
}

signup_validator = Validator(signup_schema)
