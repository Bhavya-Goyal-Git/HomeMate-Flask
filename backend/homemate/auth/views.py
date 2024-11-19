from homemate.auth import authNamespace
from ..models import db
from ..models.tables import User
from flask_restx import Resource, reqparse, fields
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, current_user
import homemate.validators as validators

registration_parser = reqparse.RequestParser()
registration_parser.add_argument('username',type=validators.username_validator,required=True, location='form')
registration_parser.add_argument('email_address',type=validators.email_validator,required=True, location='form')
registration_parser.add_argument('password',type=validators.password_validator,required=True, location='form')
registration_parser.add_argument('role',type=validators.role_validator,required=True, location='form')

User_model = authNamespace.model("User_model",{
    "username":fields.String,
    "email_address":fields.String,
    "role":fields.String,
    "date_joined":fields.Date
})

@authNamespace.route("/signup")
class SignUp(Resource):
    @authNamespace.expect(registration_parser)
    @authNamespace.marshal_with(User_model)
    def post(self):
        """Register a new user into the platform"""
        
        userdata = registration_parser.parse_args()
        newuser = User(username=userdata["username"],password=userdata["password"],email_address=userdata["email_address"],role=userdata["role"])
        try:
            db.session.add(newuser)
            db.session.commit()
        except:
            authNamespace.abort(404,"Some error occured")
        return newuser, 201
     
login_parser = reqparse.RequestParser()
login_parser.add_argument("username",type=str,required=True,location="form")
login_parser.add_argument("password",type=str,required=True,location="form")
   
@authNamespace.route("/login")
class Login(Resource):
    @authNamespace.expect(login_parser)
    def post(self):
        """Generate a new JWT pair"""
        
        userdata = login_parser.parse_args()
        user = User.query.filter_by(username=userdata["username"]).one_or_none()
        if not user:
            authNamespace.abort(401,"No such username exists.")
        if not user.check_password(userdata["password"]):
            authNamespace.abort(401,"Incorrect Password!")
        access_token = create_access_token(identity=user)
        refresh_token = create_refresh_token(identity=user)
        return {"access_token":access_token,"refresh_token":refresh_token}, 201
    
@authNamespace.route("/refresh")
class RefreshLogin(Resource):
    @jwt_required(refresh=True)
    def get(self):
        """Get a new Access Token using Refresh Token"""
        
        access_token = create_access_token(identity=current_user)
        return {"access_token":access_token}
