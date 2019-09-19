from cerberus import Validator

summarizer_schema = {
    'title': {
        'type': 'string',
        'required': True
    },
    'text': {
        'type': 'string',
        'required': True
    },
    'sentences_number': {
        'type': 'string'
    }
}

summarizer_validator = Validator(summarizer_schema)
