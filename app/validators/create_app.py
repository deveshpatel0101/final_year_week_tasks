from cerberus import Validator

create_app_schema = {
    'data': {
        'type': 'dict',
        'schema': {
            'name': {
                'type': 'string',
                'minlength': 3,
                'required': True
            },
            'allowed_apis': {
                'type': 'list',
                'schema': {
                    'type': 'string',
                    'regex': '^(translator)$|^(entities)|^(sentiment)$|^(summarizer)$'
                },
                'maxlength': 2,
                'required': True
            },
            'requests': {
                'type': 'list',
                'required': True,
                'maxlength': 0
            },
            'created_at': {
                'type': 'integer',
                'required': False
            }
        }
    }
}

create_app_validator = Validator(create_app_schema)
