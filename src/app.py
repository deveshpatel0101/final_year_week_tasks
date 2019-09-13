from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS

from routes.signup import SignUp
from routes.signin import SignIn
from routes.create_app import CreateApp
from routes.nlps.lang_trans import Translate
from routes.nlps.sentiment import Sentiment
from routes.nlps.entity_extract import EntityExtraction
from routes.nlps.summarization import Summarizer


app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(SignUp, '/user/signup')
api.add_resource(SignIn, '/user/signin')
api.add_resource(CreateApp, '/create/app')
api.add_resource(Translate, '/nlps/translator')
api.add_resource(Sentiment, '/nlps/sentiment')
api.add_resource(EntityExtraction, '/nlps/entities')
api.add_resource(Summarizer, '/nlps/summarizer')

app.run(port=5000, debug=True)
