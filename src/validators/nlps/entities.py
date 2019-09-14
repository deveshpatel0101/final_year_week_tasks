from cerberus import Validator

entities_schema = {
    'text': {
        'type': 'string'
    }
}

entities_validator = Validator(entities_schema)
