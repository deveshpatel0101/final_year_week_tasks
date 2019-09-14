from cerberus import Validator

summarizer_schema = {
    'title': {
        'type': 'string'
    },
    'text': {
        'type': 'string'
    },
    'sentences_number': {
        'type': 'string'
    }
}

summarizer_validator = Validator(summarizer_schema)
