from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
from dotenv import load_dotenv
import os

from app.routes.signup import SignUp
from app.routes.signin import SignIn
from app.routes.create_app import CreateApp
from app.routes.usage import Usage
from app.routes.token import Token
from app.routes.nlps.translator import Translate
from app.routes.nlps.sentiment import Sentiment
from app.routes.nlps.entities import EntityExtraction
from app.routes.nlps.summarization import Summarizer
from app.db.redis import rds, rds_for_db, host2, port2, password2, db2

app = Flask(__name__)
CORS(app)
api = Api(app)

if not os.getenv('PRODUCTION'):
    load_dotenv()

print('TEST1: ', rds.set('myset', 'something'))
print('TEST2: ', rds.migrate(host=host2, port=port2, keys='myset',
                  destination_db=db2, copy=False, replace=False, auth=password2, timeout=5000))

api.add_resource(SignUp, '/user/signup')
api.add_resource(SignIn, '/user/signin')
api.add_resource(CreateApp, '/create/app')
api.add_resource(Usage, '/apps/usage')
api.add_resource(Token, '/app/token')
api.add_resource(Translate, '/nlps/translator')
api.add_resource(Sentiment, '/nlps/sentiment')
api.add_resource(EntityExtraction, '/nlps/entities')
api.add_resource(Summarizer, '/nlps/summarizer')
