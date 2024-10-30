from flask import Flask
from .models import db, bcrypt
from .config import Config
from flask_restx import Api
from .auth import authNamespace


app = Flask(__name__)
app.config.from_object(Config)
bcrypt.init_app(app)
db.init_app(app)
api = Api(app)
api.add_namespace(authNamespace)