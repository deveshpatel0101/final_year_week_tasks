from cerberus import Validator

translator_schema = {
    'text': {
        'type': 'string',
        'required': True
    },
    'lang': {
        'type': 'string',
        'regex': '^([a-z]{2,3})(-)([a-z]{2,3})$',
        'required': True
    }
}

translator_validator = Validator(translator_schema)
