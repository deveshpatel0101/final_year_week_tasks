from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
from dotenv import load_dotenv
import os

from app.routes.signup import SignUp
from app.routes.signin import SignIn
from app.routes.create_app import CreateApp
from app.routes.nlps.translator import Translate
from app.routes.nlps.sentiment import Sentiment
from app.routes.nlps.entities import EntityExtraction
from app.routes.nlps.summarization import Summarizer

app = Flask(__name__)
CORS(app)
api = Api(app)

if not os.getenv('PRODUCTION'):
    load_dotenv()


api.add_resource(SignUp, '/user/signup')
api.add_resource(SignIn, '/user/signin')
api.add_resource(CreateApp, '/create/app')
api.add_resource(Translate, '/nlps/translator')
api.add_resource(Sentiment, '/nlps/sentiment')
api.add_resource(EntityExtraction, '/nlps/entities')
api.add_resource(Summarizer, '/nlps/summarizer')
