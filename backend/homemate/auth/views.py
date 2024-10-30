from homemate.auth import authNamespace
from flask_restx import Resource

@authNamespace.route("/singup")
class SignUp(Resource):
    def get(self):
        return {"Hello":"World"}


@authNamespace.route("/login")
class Login(Resource):
    def post(self):
        return {"Hello":"World"}
    
