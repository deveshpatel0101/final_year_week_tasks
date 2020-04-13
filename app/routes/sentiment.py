from flask import request
from flask_restful import Resource
import os

from app.models.sentiment_analysis.sentiment_mod import sentiment


class Sentiment(Resource):
    def post(self):
        data = request.get_json()
        output = sentiment(data['input'])
        return {'error': False, 'results': {'sentiment': output[0], 'accuracy': output[1]}}
