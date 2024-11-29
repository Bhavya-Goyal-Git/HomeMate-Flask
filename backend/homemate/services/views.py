from flask_restx import Resource, fields, reqparse
from . import serviceNs
import homemate.validators as validators
from ..models import db
from ..models.tables import Service, ServiceCategory, ServiceRequest, Professional, Customer
from flask_jwt_extended import current_user, jwt_required
from sqlalchemy import desc
from homemate import cache

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

@cache.memoize(60)
def getservicebyid(id):
    return Service.query.filter_by(id=id).one_or_none()

@serviceNs.route("")
class ServiceClass(Resource):
    @jwt_required()
    @cache.cached(60)
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
        serv = getservicebyid(id)
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
    @cache.cached(60)
    @serviceNs.marshal_list_with(categories_model)
    def get(self):
        """Get all service Categories"""
        cats = ServiceCategory.query.all()
        return cats,200

serviceRequest_parser = reqparse.RequestParser()
serviceRequest_parser.add_argument("professional_id",location="json",required=True,type=int)
serviceRequest_parser.add_argument("dateofservice",location="json",required=True,type=validators.date_validator)

@serviceNs.route("/request")
class ServReq(Resource):
    @jwt_required()
    @serviceNs.expect(serviceRequest_parser)
    def post(self):
        """Create a service request"""
        if current_user.role!="customer":
            serviceNs.abort(401,"Some error occured",errors={"unauthorized":"You are not authorized to make a service request"})
        sdata = serviceRequest_parser.parse_args()
        prof = Professional.query.filter_by(id=sdata["professional_id"]).one_or_none()
        if not prof:
            serviceNs.abort(404,"Some error occured",errors={"service":"No professional found with given id"})
        snew = ServiceRequest()
        snew.customer = current_user.customer_data
        snew.professional=prof
        snew.dateofcompletion = sdata["dateofservice"]
        snew.status="booked"
        try:
            db.session.add(snew)
            db.session.commit()
        except:
            db.session.rollback()
            serviceNs.abort(404,"Some error occured",errors={"database":"Database error occured"})
        return {"success":"service request made"},200

serviceRequest_model = serviceNs.model("ServiceRequestModel",{
    "id":fields.Integer,
    "customer_name":fields.String,
    "professional_name":fields.String,
    "professional_id":fields.Integer,
    "service_name":fields.String,
    "dateofrequest":fields.Date,
    "dateofcompletion":fields.Date,
    "status":fields.String,
    "work_units":fields.Float,
    "parts_cost":fields.Float,
    "total_bill":fields.Float
})

@serviceNs.route("/requests/<string:role>/<int:id>")
class ServReqss(Resource):
    @jwt_required()
    @serviceNs.marshal_list_with(serviceRequest_model)
    def get(self,role,id):
        """Get All service requests for a professional (pid) or a customer (cid)"""
        if current_user.role != role or (current_user.role=="customer" and current_user.customer_data.id!=id) or (current_user.role=="professional" and current_user.professional_data.id!=id):
            serviceNs.abort(401,"Some error occured",errors={"unauthorized":"You are not authorized to view this service request"})
        reqs = []
        if role=="customer":
            reqs = db.session.query(ServiceRequest,Service.title,Professional,Customer.name).join(ServiceRequest.professional).join(ServiceRequest.customer).join(Professional.service_type).filter(ServiceRequest.customer_id==id).order_by(desc(ServiceRequest.dateofcompletion)).all()
        else: #professional
            reqs = db.session.query(ServiceRequest,Service.title,Professional,Customer.name).join(ServiceRequest.professional).join(ServiceRequest.customer).join(Professional.service_type).filter(ServiceRequest.professional_id==id).order_by(desc(ServiceRequest.dateofcompletion)).all()
        dataToSend = []
        for sreq,serv,prof,cust in reqs:
            dataToSend.append({
                "id":sreq.id,
                "customer_name":cust,
                "professional_name":prof.name,
                "professional_id":prof.id,
                "service_name":serv,
                "dateofrequest":sreq.dateofrequest,
                "dateofcompletion":sreq.dateofcompletion,
                "status":sreq.status,
                "work_units":sreq.work_units if sreq.work_units else -1,
                "parts_cost":sreq.parts_cost if sreq.parts_cost else -1,
                "total_bill":sreq.total_bill if sreq.total_bill else -1
            })
        return dataToSend,200

sreq_parser = reqparse.RequestParser()
sreq_parser.add_argument("status",required=True,location="json",type=validators.serviceStatus_validator)
sreq_parser.add_argument("work_units",location="json",type=float)
sreq_parser.add_argument("parts_cost",location="json",type=float)

@serviceNs.route("/request/<int:sid>")
class ServREQ(Resource):
    @jwt_required()
    @serviceNs.expect(sreq_parser)
    def put(self,sid):
        """Make changes to Service Request using service id"""
        sdata = ServiceRequest.query.filter_by(id=sid).one_or_none()
        flag=False
        if not sdata:
            serviceNs.abort(404,"Some error occured",errors={"service":"No Service found with given id"})
        sreq = sreq_parser.parse_args()
        if current_user.role=="customer" and current_user.customer_data.id==sdata.customer_id:
            if sdata.status == "booked" or sdata.status == "accepted": # can be cancelled by customer
                if sreq["status"]!="cancelled":
                    serviceNs.abort(404,"Some error occured",errors={"Error":"Invalid change requested!"})
                sdata.status = "cancelled"
                flag=True
            elif sdata.status == "served": #can be completed by customer
                if sreq["status"]!="completed":
                    serviceNs.abort(404,"Some error occured",errors={"Error":"Invalid change requested!"})
                sdata.status = "completed"
                flag=True
            else: 
                serviceNs.abort(404,"Some error occured",errors={"service":"Can't make changes to this service request!"})
        elif current_user.role=="professional" and current_user.professional_data.id==sdata.professional_id:
            if sdata.status == "booked": #accept or reject by worker
                if sreq["status"] not in ["accepted","rejected"]:
                    serviceNs.abort(404,"Some error occured",errors={"Error":"Invalid change requested!"})
                sdata.status = sreq["status"]
                flag=True
            elif sdata.status == "accepted": #served by worker
                if sreq["status"] != "served":
                    serviceNs.abort(404,"Some error occured",errors={"Error":"Invalid change requested!"})
                if not sreq.get("work_units") or not sreq.get("parts_cost"):
                    serviceNs.abort(404,"Some error occured",errors={"Error":"Data insufficient to serve the request!"})
                sdata.status = "served"
                sdata.work_units = sreq["work_units"]
                sdata.parts_cost = sreq["parts_cost"]
                #total calculation
                prof = sdata.professional
                sdata.total_bill = prof.service_type.base_price + (sdata.work_units * prof.fees) + sdata.parts_cost
                flag=True
            else:
                serviceNs.abort(404,"Some error occured",errors={"service":"Can't make changes to this service request!"})
        else:
            serviceNs.abort(401,"Some error occured",errors={"unauthorized":"You are not authorized to change this service request"})
        if flag:
            try:
                db.session.add(sdata)
                db.session.commit()
            except:
                db.session.rollback()
                serviceNs.abort(404,"Some error occured",errors={"database":"Database error occured"})
        return {"success":"changes made successfully!"},200

    @jwt_required()
    def delete(self,sid):
        """Delete a Cancelled or Rejected Service Request"""
        sdata = ServiceRequest.query.filter_by(id=sid).one_or_none()
        if not sdata:
            serviceNs.abort(404,"Some error occured",errors={"service":"No Service found with given id"})
        if current_user.role!="customer" or sdata.customer_id!=current_user.customer_data.id:
            serviceNs.abort(401,"Some error occured",errors={"unauthorized":"You are not authorized to delete this service request"})
        if sdata.status not in ["rejected","cancelled"]:
            serviceNs.abort(401,"Some error occured",errors={"unauthorized":"This service request can't be deleted"})
        try:
            db.session.delete(sdata)
            db.session.commit()
        except:
            db.session.rollback()
            serviceNs.abort(404,"Some error occured",errors={"database":"Database error occured"})
        return {"success":"service request deleted"},200

sreq_bill_model = serviceNs.model("ServiceRequestBill",{
    "base_price":fields.Float,
    "work_units":fields.Float,
    "worker_fee":fields.Float,
    "worker_fee_unit":fields.String,
    "parts_cost":fields.Float,
    "total_bill":fields.Float
})
@serviceNs.route("/bill/<int:sid>")
class SBill(Resource):
    @jwt_required()
    @serviceNs.marshal_with(sreq_bill_model)
    def get(self,sid):
        """Get bill details of a Served or Completed Service Request by sid"""
        sdata = ServiceRequest.query.filter_by(id=sid).one_or_none()
        if not sdata:
            serviceNs.abort(404,"Some error occured",errors={"service":"No Service found with given id"})
        if sdata.status not in ["served","completed"]:
            serviceNs.abort(401,"Some error occured",errors={"service":"Bill can't be generated for this service request"})
        prof = sdata.professional
        d = {
            "base_price":prof.service_type.base_price,
            "work_units":sdata.work_units,
            "worker_fee":prof.fees,
            "worker_fee_unit":prof.fees_unit,
            "parts_cost":sdata.parts_cost,
            "total_bill":sdata.total_bill
        }
        return d,200
        