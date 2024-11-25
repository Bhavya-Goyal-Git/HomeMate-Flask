from homemate import api
from flask_restx import Resource
from flask_jwt_extended import jwt_required, current_user
from .commonFields import User_model

@api.route("/userdata")
class UserData(Resource):
    
    @jwt_required()
    @api.marshal_with(User_model)
    def get(self):
        """Get a user's basic data with JWT"""
        return current_user,200