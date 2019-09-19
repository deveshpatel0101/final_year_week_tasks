from cerberus import Validator

entities_schema = {
    'text': {
        'type': 'string',
        'required': True
    }
}

entities_validator = Validator(entities_schema)
