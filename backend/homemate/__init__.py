from flask import Flask
from .models import db, bcrypt, jwt
from .config import Config
from flask_restx import Api
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
bcrypt.init_app(app)
db.init_app(app)
jwt.init_app(app)
CORS(app)

import homemate.asyncJobs as jobs
celery = jobs.celery
celery.conf.update(
    broker_url = app.config["CELERY_BROKER_URL"],
    result_backend = app.config["CELERY_RESULT_BACKEND"]
)
celery.Task = jobs.ContextTask

api = Api(app,title="HomeMate Platform API",description="A REST API for backend of HomeMate, a platform where service professionals and customers can register and find each other!",authorizations={
    "Bearer Auth":{
        "type":"apiKey",
        "in":"header",
        "name":"Authorization",
        "description":"Add a JWT with ** Bearer &lt;JWT&gt; to authorize"
    }}, security="Bearer Auth")

from .auth import authNamespace
from .customer import customerNs
from .professional import professNs
from .services import serviceNs

api.add_namespace(authNamespace)
api.add_namespace(customerNs)
api.add_namespace(professNs)
api.add_namespace(serviceNs)
import homemate.commonRoutes