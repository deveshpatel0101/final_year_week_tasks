from cerberus import Validator

signup_schema = {
    'email': {
        'type': 'string',
        'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    },
    'fname': {
        'type': 'string',
        'minlength': 3,
    },
    'lname': {
        'type': 'string',
        'minlength': 3,
    },
    'password': {
        'type': 'string',
        'regex': '^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).{4,}$'
    },
    'cpassword': {
        'type': 'string',
        'regex': '^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).{4,}$'
    },
    'account_type': {
        'type': 'string',
        'regex': '^(free)$'
    },
    'applications': {
        'type': 'list',
        'maxlength': 0
    }
}

signup_validator = Validator(signup_schema)
