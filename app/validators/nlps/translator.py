from cerberus import Validator

translator_schema = {
    'text': {
        'type': 'string'
    },
    'lang': {
        'type': 'string',
        'regex': '^([a-z]{2,3})(-)([a-z]{2,3})$'
    }
}

translator_validator = Validator(translator_schema)
