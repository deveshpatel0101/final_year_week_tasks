from flask import Flask, jsonify
from flask_restful import Api

from routes.signup import SignUp
from routes.signin import SignIn
from routes.nlps.lang_trans import Translate

app = Flask(__name__)
api = Api(app)

api.add_resource(SignUp, '/user/signup')
api.add_resource(SignIn, '/user/signin')
api.add_resource(Translate, '/nlps/translator')


app.run(port=5000, debug=True)
