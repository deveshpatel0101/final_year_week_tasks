from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
from dotenv import load_dotenv
import os

from app.routes.translator import Translate
from app.routes.sentiment import Sentiment
from app.routes.entities import EntityExtraction
from app.routes.summarization import Summarizer

app = Flask(__name__)
CORS(app)
api = Api(app)

if not os.getenv('PRODUCTION'):
    load_dotenv()

api.add_resource(Translate, '/translator')
api.add_resource(Sentiment, '/sentiment')
api.add_resource(EntityExtraction, '/entities')
api.add_resource(Summarizer, '/summarizer')
