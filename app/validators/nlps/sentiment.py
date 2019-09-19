from cerberus import Validator

sentiment_schema = {
    'text': {
        'type': 'string',
        'required': True
    }
}

sentiment_validator = Validator(sentiment_schema)
