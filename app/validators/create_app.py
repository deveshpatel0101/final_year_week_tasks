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
                'minlength': 1,
                'required': True
            },
            'requests': {
                'type': 'dict',
                'schema': {
                    'translator': {
                        'type': 'list',
                        'maxlength': 0,
                        'minlength': 0
                    },
                    'entities': {
                        'type': 'list',
                        'maxlength': 0,
                        'minlength': 0
                    },
                    'summarizer': {
                        'type': 'list',
                        'maxlength': 0,
                        'minlength': 0
                    },
                    'sentiment': {
                        'type': 'list',
                        'maxlength': 0,
                        'minlength': 0
                    }
                },
                'required': True
            },
            'created_at': {
                'type': 'integer',
                'required': False
            }
        }
    }
}

create_app_validator = Validator(create_app_schema)
