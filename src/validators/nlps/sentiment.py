from cerberus import Validator

sentiment_schema = {
    'text': {
        'type': 'string'
    }
}

sentiment_validator = Validator(sentiment_schema)
