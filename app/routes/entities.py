from flask import request
from flask_restful import Resource
import os


from app.models.named_entity_recognition.entity import find_entities


class EntityExtraction(Resource):
    def post(self):
        data = request.get_json()
        output = find_entities(data['input'])
        return {'error': False, 'results': output}
