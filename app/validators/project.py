from cerberus import Validator

create_project_schema = {
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

update_project_schema = {
    'name': {
        'type': 'string',
        'minlength': 3
    },
    'update': {
        'type': 'dict',
        'schema': {
            'name': {
                'type': 'string',
                'minlength': 3,
            },
            'allowed_apis': {
                'type': 'list',
                'schema': {
                    'type': 'string',
                    'regex': '^(translator)$|^(entities)|^(sentiment)$|^(summarizer)$'
                },
                'maxlength': 2,
                'minlength': 1,
            }
        },
        'required': True
    }
}

delete_project_schema = {
    'name': {
        'type': 'string',
        'required': True
    }
}

create_project_validator = Validator(create_project_schema)

delete_project_validator = Validator(delete_project_schema)

update_project_validator = Validator(update_project_schema)
