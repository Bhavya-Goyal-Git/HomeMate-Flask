from homemate.customer import customerNs
from flask_restx import Resource, reqparse, fields
from flask_jwt_extended import jwt_required, current_user
from ..models import db
from ..models.tables import Customer
import homemate.validators as validator
from ..commonFields import address_model

userdata_parser = reqparse.RequestParser()
userdata_parser.add_argument("name",required=True,type=validator.name_validator,location="json")
userdata_parser.add_argument("address",required=True,type=validator.address_validator,location="json")

customer_model = customerNs.model("customerModel",{
    "id":fields.Integer,
    "name":fields.String,
    "address":fields.Nested(address_model),
    "isflagged":fields.Boolean
})

@customerNs.route("/data/<int:id>")
class CustomerData(Resource):
    @jwt_required()
    @customerNs.marshal_with(customer_model)
    def get(self,id):
        """Get customer's data using id (user_id)"""
        if current_user.id != id and current_user.role !="admin":
            customerNs.abort(401,"Unauthorized",errors={"role":"You aren't authorized to access this resource"})
        cdata = Customer.query.filter_by(user_id=id).one_or_none()
        if not cdata:
            customerNs.abort(404,"Some error occured",errors={"Customer":"Customer with given id does not exist."})
        return cdata.to_dict(),200
    
    @jwt_required()
    @customerNs.expect(userdata_parser)
    @customerNs.marshal_with(customer_model)
    def post(self,id):
        """Upload Customer's data like address, name"""
        if current_user.id != id or current_user.role != "customer":
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
            db.session.rollback()
            customerNs.abort(404,"Some error occured",errors={"database":"Database error occured"})
        return newCustomer.to_dict(),201
    
    @jwt_required()
    def patch(self,id):
        """Flag or unflag a customer via id (cid)"""
        if current_user.role!="admin":
            customerNs.abort(401,"Unauthorized",errors={"role":"You aren't authorized to access this resource"})
        cust = Customer.query.filter_by(id=id).one_or_none()
        if not cust:
            customerNs.abort(404,"Some error occured",errors={"Customer":"Customer with given id does not exist."})
        cust.isflagged = not cust.isflagged
        try:
            db.session.add(cust)
            db.session.commit()
        except:
            db.session.rollback()
            customerNs.abort(404,"Some error occured",errors={"database":"Database error occured"})
        return {"success":"Customer successfully (un)flagged"},200


@customerNs.route("/data")
class AllCustData(Resource):
    
    @jwt_required()
    @customerNs.marshal_list_with(customer_model)
    def get(self):
        """Get all customer's data"""
        if current_user.role!="admin":
            customerNs.abort(401,"Unauthorized",errors={"role":"You aren't authorized to access this resource"})
        cdata = Customer.query.all()
        dataTosend = [c.to_dict() for c in cdata]
        return dataTosend,200

@customerNs.route("/<int:cid>")
class OpenCustData(Resource):
    @jwt_required()
    @customerNs.marshal_with(customer_model)
    def get(self,cid):
        """Get customer using cid"""
        cust = Customer.query.filter_by(id=cid).one_or_none()
        if not cust:
            customerNs.abort(404,"Some error occured",errors={"Customer":"Customer with given id does not exist."})
        return cust.to_dict(),200