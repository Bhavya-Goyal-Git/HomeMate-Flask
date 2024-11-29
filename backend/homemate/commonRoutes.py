from flask import send_file
from homemate import api,app
from flask_restx import Resource, fields, marshal, reqparse
from flask_jwt_extended import jwt_required, current_user
from .models import db
from .models.tables import User, Service, Professional, ServiceRequest, ProfessionalReview, Customer
from .commonFields import User_model
from sqlalchemy.sql import func
from .asyncJobs.tasks import ServiceRequestTableExport
import os

@api.route("/userdata")
class UserData(Resource):
    @jwt_required()
    @api.marshal_with(User_model)
    def get(self):
        """Get a user's basic data with JWT"""
        return current_user,200

userdata = {
    "role":fields.String,
    "count":fields.Integer
}
catcounts = {
    "cat":fields.String,
    "count":fields.Integer
}
catavg = {
    "cat":fields.String,
    "avgprice":fields.Float
}
starnum = {
    "star":fields.Integer,
    "count":fields.Integer
}
sreq = {
    "status":fields.String,
    "count":fields.Integer
}

result = {
    "userdata":fields.List(fields.Nested(userdata)),
    "service_cat_count":fields.List(fields.Nested(catcounts)),
    "service_cat_avgprice":fields.List(fields.Nested(catavg)),
    "service_cat_numprofs":fields.List(fields.Nested(catcounts)),
    "stars_dist":fields.List(fields.Nested(starnum)),
    "servReq_status":fields.List(fields.Nested(sreq)),
    "earning_perDay":fields.Raw
}

@api.route("/stats")
class AdminStats(Resource):
    @jwt_required()
    def get(self):
        """Get statistics of entire platform"""
        if current_user.role!="admin":
            api.abort(401,"Unauthorized",errors={"role":"You aren't authorized to access this resource"})
        userdata = db.session.query(User.role.label('role'), func.count(User.id).label('count')).group_by(User.role).all()
        service_cat_count = db.session.query(Service.category.label('cat'),func.count(Service.id).label('count')).group_by(Service.category).all()
        service_cat_avgprice = db.session.query(Service.category.label('cat'),func.avg(Service.base_price).label('avgprice')).group_by(Service.category).all()
        service_cat_numprofs = db.session.query(Service.category.label('cat'),func.count(Professional.id).label('count')).join(Service.professionals).group_by(Service.category).all()
        stars_dist = db.session.query(ProfessionalReview.stars.label('star'),func.count(ProfessionalReview.id).label('count')).group_by(ProfessionalReview.stars).all()
        servReq_status = db.session.query(ServiceRequest.status.label('status'),func.count(ServiceRequest.id).label('count')).group_by(ServiceRequest.status).all()
        
        d = db.session.query(ServiceRequest,Service.base_price).join(ServiceRequest.professional).join(Professional.service_type).all()
        earning_perDay = {}
        for sreq,bp in d:
            earning_perDay[sreq.dateofcompletion.strftime('%Y-%m-%d')] = earning_perDay.get(sreq.dateofcompletion.strftime('%Y-%m-%d'),0) + bp
        return marshal({
            "userdata":userdata,
            "service_cat_count":service_cat_count,
            "service_cat_avgprice":service_cat_avgprice,
            "service_cat_numprofs":service_cat_numprofs,
            "stars_dist":stars_dist,
            "servReq_status":servReq_status,
            "earning_perDay":earning_perDay
        }, result),200

argparser = reqparse.RequestParser()
argparser.add_argument("fname",location="args",required=True,type=str)

@api.route("/servicerequest/getcsv")
class GetServiceTable(Resource):
    @jwt_required()
    def post(self):
        """Admin can request a csv export of service request table here!"""
        if current_user.role!="admin":
            api.abort(401,"Unauthorized",errors={"role":"You aren't authorized to access this resource"})
        task = ServiceRequestTableExport.apply_async()
        return {"job_id":task.id},202
    
    @jwt_required(refresh=True)
    def get(self):
        """Get Generated Service Request CSV by filename"""
        if current_user.role!="admin":
            api.abort(401,"Unauthorized",errors={"role":"You aren't authorized to access this resource"})
        f = argparser.parse_args()
        file_path = os.path.join(app.root_path,"ServiceRequestCSV",f["fname"])
        if not os.path.exists(file_path):
            api.abort(404,"Some error occured",errors={"Admin":"Submitted document could not be found!"})
        return send_file(
            file_path,
        )