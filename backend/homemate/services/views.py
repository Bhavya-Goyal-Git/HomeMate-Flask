from flask_restx import Resource, fields, reqparse
from . import serviceNs
import homemate.validators as validators
from ..models import db
from ..models.tables import Service, ServiceCategory
from flask_jwt_extended import current_user, jwt_required

service_parser = reqparse.RequestParser()
service_parser.add_argument("title",type=validators.service_title_validator,required=True,location="json")
service_parser.add_argument("base_price",type=validators.price_validator,required=True,location="json")
service_parser.add_argument("description",type=str,location="json")
service_parser.add_argument("category",type=str,required=True,location="json")

service_model = serviceNs.model("serviceModel",{
    "id":fields.Integer,
    "title":fields.String,
    "base_price":fields.Float,
    "description":fields.String,
    "category":fields.String
})

@serviceNs.route("")
class ServiceClass(Resource):
    @jwt_required()
    @serviceNs.marshal_list_with(service_model)
    def get(self):
        """Get all Services data"""
        services = Service.query.all()
        return services,200
    
    @jwt_required()
    @serviceNs.expect(service_parser)
    @serviceNs.marshal_with(service_model)
    def post(self):
        """Add a new Service to the platform"""
        
        if current_user.role != "admin":
            serviceNs.abort(401,"Some error occured",errors={"unauthorized":"You are not authorized to create a service"})
        servdata = service_parser.parse_args()
        newService = Service(title=servdata["title"],base_price=servdata["base_price"],category=servdata["category"])
        if servdata.get("description") is not None:
            newService.description = servdata["description"]
        try:
            db.session.add(newService)
            db.session.commit()
        except:
            db.session.rollback()
            serviceNs.abort(404,"Some error occured",errors={"database":"Database error occured"})
        return newService,201
    
service_parser2 = service_parser.copy()
service_parser2.replace_argument("title",type=validators.service_title_validator_old,required=True,location="json")
@serviceNs.route("/<int:id>")
class SingleService(Resource):
    
    @jwt_required()
    @serviceNs.marshal_with(service_model)
    def get(self,id):
        """Get data of a service by id"""
        serv = Service.query.filter_by(id=id).one_or_none()
        if not serv:
            serviceNs.abort(404,"Some error occured",errors={"service":f"No sevice found with id:{id}"})
        return serv,200
    
    @jwt_required()
    def delete(self,id):
        """Delete a service by id"""
        if current_user.role!="admin":
            serviceNs.abort(401,"Some error occured",errors={"unauthorized":"You are not authorized to delete a service"})
        serv = Service.query.filter_by(id=id).one_or_none()
        if not serv:
            serviceNs.abort(404,"Some error occured",errors={"service":f"No sevice found with id:{id}"})
        if len(serv.professionals)>0:
            serviceNs.abort(404,"Some error occured",errors={"service":"Can't delete service! There are running requests of this service."})
        try:
            db.session.delete(serv)
            db.session.commit()
        except:
            db.session.rollback()
            serviceNs.abort(404,"Some error occured",errors={"database":"Database error occured"})
        return {"success":"Service deleted!"},200
    
    @jwt_required()
    @serviceNs.expect(service_parser2)
    @serviceNs.marshal_with(service_model)
    def put(self,id):
        """Edit service details by id"""
        if current_user.role!="admin":
            serviceNs.abort(401,"Some error occured",errors={"unauthorized":"You are not authorized to edit a service"})
        serv = Service.query.filter_by(id=id).one_or_none()
        if not serv:
            serviceNs.abort(404,"Some error occured",errors={"service":f"No sevice found with id:{id}"})
        servdata = service_parser2.parse_args()
        serv.title = servdata["title"]
        serv.base_price = servdata["base_price"]
        serv.category = servdata["category"]
        if servdata.get("description") is not None:
            serv.description = servdata["description"]
        try:
            db.session.add(serv)
            db.session.commit()
        except:
            db.session.rollback()
            serviceNs.abort(404,"Some error occured",errors={"database":"Database error occured"})
        return serv,200
  
categories_model = serviceNs.model("ServiceCategory",{
    "id":fields.Integer,
    "title":fields.String
})

@serviceNs.route("/categories")
class ServiceCats(Resource):
    
    @jwt_required()
    @serviceNs.marshal_list_with(categories_model)
    def get(self):
        """Get all service Categories"""
        cats = ServiceCategory.query.all()
        return cats,200