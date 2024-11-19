from flask import Flask
from .models import db, bcrypt, jwt
from .config import Config
from flask_restx import Api
from .auth import authNamespace
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
bcrypt.init_app(app)
db.init_app(app)
jwt.init_app(app)
CORS(app)
api = Api(app)
api.add_namespace(authNamespace)
