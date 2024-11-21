from homemate.customer import customerNs
from flask_restx import Resource, reqparse, fields
from flask_jwt_extended import jwt_required, current_user
from ..models import db
from ..models.tables import Customer
import homemate.validators as validator
from ..commonFields import address_model

userdata_parser = reqparse.RequestParser()
userdata_parser.add_argument("name",required=True,type=validator.name_validator,location="form")
userdata_parser.add_argument("address",required=True,type=validator.address_validator,location="form")

customer_model = customerNs.model("customerModel",{
    "id": fields.Integer,
    "name":fields.String,
    "address":fields.Nested(address_model),
    "isflagged":fields.Boolean
})

@customerNs.route("/data/<int:id>")
class CustomerData(Resource):
    
    @jwt_required()
    @customerNs.expect(userdata_parser)
    @customerNs.marshal_with(customer_model)
    def post(self,id):
        """Upload Customer's data like address, name"""
        if current_user.id != id:
            customerNs.abort(401,"Unauthorized",errors={"role":"You aren't authorized to access this resource"})
        cdata = userdata_parser.parse_args()
        newCustomer = Customer(name=cdata["name"],user_id=id)
        newCustomer.base_address = cdata["address"]["base_address"]
        newCustomer.city = cdata["address"]["city"]
        newCustomer.pincode = cdata["address"]["pincode"]
        newCustomer.state = cdata["address"]["state"]
        try:
            db.session.add(newCustomer)
            db.session.commit()
        except:
            customerNs.abort(404,"Some error occured",errors={"database":"Database error occured"})
        return newCustomer,201
        
        

