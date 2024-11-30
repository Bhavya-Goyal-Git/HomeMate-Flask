from homemate.professional import professNs
from homemate import app,cache
from flask import send_file
from flask_restx import Resource, reqparse, fields
from flask_jwt_extended import jwt_required, current_user
from ..models import db
from ..models.tables import Professional, Service, ProfessionalReview, Customer, ServiceRequest
import homemate.validators as validator
from ..commonFields import address_model
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import os
from sqlalchemy import or_,desc
import uuid

profess_parser = reqparse.RequestParser()
profess_parser.add_argument("name",type=validator.name_validator,required=True,location="form")
profess_parser.add_argument("description",type=str,location="form")
profess_parser.add_argument("base_address",type=str,required=True,location="form")
profess_parser.add_argument("city",type=str,required=True,location="form")
profess_parser.add_argument("state",type=str,required=True,location="form")
profess_parser.add_argument("pincode",type=validator.validate_pincode,required=True,location="form")
profess_parser.add_argument("contact_no",type=validator.mobile_num_validator,required=True,location="form")
profess_parser.add_argument("experience",type=int,required=True,location="form")
profess_parser.add_argument("service_id",type=int,required=True,location="form")
profess_parser.add_argument("fees",type=float,required=True,location="form")
profess_parser.add_argument("fees_unit",type=str,required=True,location="form")
profess_parser.add_argument("documents",type=FileStorage,required=True,location="files")

profess_model = professNs.model("ProfessionalModel",{
    "id":fields.Integer,
    "name":fields.String,
    "description":fields.String,
    "address":fields.Nested(address_model),
    "contact_no":fields.String,
    "isflagged":fields.Boolean,
    "isverified":fields.String,
    "experience":fields.Integer,
    "rating":fields.Integer,
    "num_raters":fields.Integer,
    "service_id":fields.Integer,
    "fees":fields.Float,
    "fees_unit":fields.String,
})

patch_parser = reqparse.RequestParser()
patch_parser.add_argument("status",location="json",type=str)

@cache.memoize(60)
def getprofessionalbyid(id):
    return Professional.query.filter_by(user_id=id).one_or_none()
@cache.memoize(60)
def getprofessionalbypid(pid):
    return Professional.query.filter_by(id=pid).one_or_none()
@cache.cached(timeout=60,key_prefix='all_professionals')
def get_all_professionals():
    return Professional.query.all()
@cache.memoize(60)
def profReviewbypid(id):
    return db.session.query(ProfessionalReview,Customer).join(ProfessionalReview.customer).filter(ProfessionalReview.professional_id==id).order_by(desc(ProfessionalReview.dateofreview)).all()

@professNs.route("/data/<int:id>")
class ProfessionalData(Resource):
    
    @jwt_required()
    @professNs.marshal_with(profess_model)
    def get(self,id):
        """Get Professional's data using id (User id)"""
        if current_user.id != id and current_user.role !="admin":
            professNs.abort(401,"Unauthorized",errors={"role":"You aren't authorized to access this resource"})
        pdata = getprofessionalbyid(id)
        if not pdata:
            professNs.abort(404,"Some error occured",errors={"Professional":"Professional with given id does not exist."})
        return pdata.to_dict(),200
    
    @jwt_required()
    @professNs.expect(profess_parser)
    @professNs.marshal_with(profess_model)
    def post(self,id):
        """Upload Service Professional's data like address, name etc."""
        if current_user.id != id or current_user.role!="professional":
            professNs.abort(401,"Unauthorized",errors={"role":"You aren't authorized to access this resource"})
            
        pdata = profess_parser.parse_args()
        doc_file = pdata["documents"]
        if doc_file.filename == '' or doc_file.filename[-3:].lower()!="pdf":
            professNs.abort(404,"Bad File",errors={"file":"Document file must be a pdf!"})
        fname = str(uuid.uuid1()) + secure_filename(doc_file.filename)
        doc_file.save(os.path.join(app.root_path,"uploads",fname))
        
        newprofessional = Professional(user_id=id,name=pdata["name"])
        newprofessional.base_address = pdata["base_address"]
        newprofessional.city = pdata["city"]
        newprofessional.pincode = pdata["pincode"]
        newprofessional.state = pdata["state"]
        if pdata.get("description") is not None:
            newprofessional.description = pdata["description"]
        newprofessional.contact_no = pdata["contact_no"]
        newprofessional.experience = pdata["experience"]
        newprofessional.service_id = pdata["service_id"]
        newprofessional.fees = pdata["fees"]
        newprofessional.fees_unit = pdata["fees_unit"]
        newprofessional.submitted_doc = fname
        try:
            db.session.add(newprofessional)
            db.session.commit()
        except Exception as e:
            print(e)
            print(str(e))
            db.session.rollback()
            professNs.abort(404,"Some error occured",errors={"database":"Database error occured"})
        return newprofessional.to_dict(),201
    
    @jwt_required()
    @professNs.expect(patch_parser)
    def patch(self,id):
        """Update professional's Document approval by id (pid) or flag a professional (pid)"""
        if current_user.role != "admin":
            professNs.abort(401,"Unauthorized",errors={"role":"You aren't authorized to access this resource"})
        pdata = Professional.query.filter_by(id=id).one_or_none()
        if not pdata:
            professNs.abort(404,"Some error occured",errors={"Professional":"Professional with given id does not exist."})
        st = patch_parser.parse_args()
        resultStr="professional document approval status updated"
        if st.get("status"):
            pdata.isverified = st["status"]
        else:
            pdata.isflagged = not pdata.isflagged
            resultStr=f"Professional successfully (un)flagged" 
        try:
            db.session.add(pdata)
            db.session.commit()
        except:
            db.session.rollback()
            professNs.abort(404,"Some error occured",errors={"database":"Database error occured"})
        return {"success":resultStr},200

query_data_parser = reqparse.RequestParser()
query_data_parser.add_argument("unverified",type=bool,location="args")

@professNs.route("/data")
class AllProfessData(Resource):
    
    @jwt_required()
    @professNs.expect(query_data_parser)
    @professNs.marshal_list_with(profess_model)
    def get(self):
        """Get Data of all professionals"""
        if current_user.role!="admin":
            professNs.abort(401,"Unauthorized",errors={"role":"You aren't authorized to access this resource"})
        qdata = query_data_parser.parse_args()
        pdata = None
        if qdata.get("unverified"):
            pdata = Professional.query.filter_by(isverified="pending").all()
        else:
            pdata = get_all_professionals()
        dataTosend = [p.to_dict() for p in pdata]
        return dataTosend,200
    
@professNs.route("/docs/<int:id>")
class ProfessionalDocs(Resource):
    
    @jwt_required()
    def get(self,id):
        """Get Professional's submitted document using id (pid)"""
        if (current_user.role == "professional" and current_user.professional_data.id!=id) and current_user.role!="admin":
            professNs.abort(401,"Unauthorized",errors={"role":"You aren't authorized to access this resource"})
        pdata = Professional.query.filter_by(id=id).one_or_none()
        if not pdata:
            professNs.abort(404,"Some error occured",errors={"Professional":"Professional with given id does not exist."})
        file_path = os.path.join(app.root_path,"uploads",pdata.submitted_doc)
        if not os.path.exists(file_path):
            professNs.abort(404,"Some error occured",errors={"Professional":"Submitted document could not be found!"})
        return send_file(
            file_path,
            mimetype='application/pdf'
        )

searchquery_parser = reqparse.RequestParser()
searchquery_parser.add_argument("q",required=True,type=str,location="args")

@professNs.route("/search")
class SearchProfessional(Resource):
    @jwt_required()
    @professNs.expect(searchquery_parser)
    @professNs.marshal_list_with(profess_model)
    def get(self):
        """Search approved professionals via professional's name, service or service category"""
        searchq = searchquery_parser.parse_args()
        searchq = searchq["q"]
        searchq = validator.clean_searchquery(searchq)
        if len(searchq)==0:
            professNs.abort(404,"Some error occured",errors={"Professional":"Search Query Empty"})
        pdata = db.session.query(Professional).join(Professional.service_type).filter(Professional.isverified == "approved").filter(or_(
            Professional.name.ilike(searchq),
            Service.title.ilike(searchq),
            Service.category.ilike(searchq)
            )).all()
        dataTosend = [p.to_dict() for p in pdata]
        return dataTosend,200

review_parser = reqparse.RequestParser()
review_parser.add_argument("stars",required=True,type=int,location="json")
review_parser.add_argument("review",required=True,type=str,location="json")

review_model = professNs.model("ProfessionalReview",{
    "id":fields.Integer,
    "customer_name":fields.String,
    "stars":fields.Integer,
    "review":fields.String,
    "dateofreview":fields.Date
})

@professNs.route("/review/<int:id>")
class ProfReviews(Resource):
    @jwt_required()
    @professNs.marshal_list_with(review_model)
    def get(self,id):
        """Get all reviews of a professional by id (pid)"""
        rdata = profReviewbypid(id)
        dataToSend= []
        for entry,cust in rdata:
            dataToSend.append({"id":entry.id,"customer_name":cust.name,"stars":entry.stars,"review":entry.review,"dateofreview":entry.dateofreview})
        return dataToSend,200
    
    @jwt_required()
    @professNs.expect(review_parser)
    def post(self,id):
        """Review a service professional by id (pid)"""
        if current_user.role!="customer":
            professNs.abort(401,"Unauthorized",errors={"role":"You aren't authorized to access this resource"})
        prof = Professional.query.filter_by(id=id).one_or_none()
        if not prof:
            professNs.abort(404,"Some error occured",errors={"Professional":"Professional with given id does not exist."})
        rdata = review_parser.parse_args()
        rnew = ProfessionalReview(customer_id=current_user.customer_data.id,professional_id=id,stars=rdata["stars"],review=rdata["review"])
        prof.rating += rdata["stars"]
        prof.num_raters +=1
        try:
            db.session.add_all([rnew,prof])
            db.session.commit()
        except:
            db.session.rollback()
            professNs.abort(404,"Some error occured",errors={"database":"Database error occured"})
        return {"success":"Reviewed Professional"},201

@professNs.route("/<int:pid>")
class OpenProfData(Resource):
    @jwt_required()
    @professNs.marshal_with(profess_model)
    def get(self,pid):
        """Get professional using pid"""
        pdata = getprofessionalbypid(pid)
        if not pdata:
            professNs.abort(404,"Some error occured",errors={"Professional":"Professional with given id does not exist."})
        return pdata.to_dict(),200

pstat_model = professNs.model("ProfessionalStats1",{
    "status":fields.String,
    "daterecieve":fields.Date,
    "date":fields.Date,
    "earning":fields.Float
})
pstat_model2 = professNs.model("ProfessionalStats2",{
    "date":fields.Date(attribute='dateofreview'),
    "stars":fields.Integer
})

@professNs.route("/servicestats")
class PStat(Resource):
    @jwt_required()
    @professNs.marshal_list_with(pstat_model)
    def get(self):
        """Get service related stats of professional"""
        if current_user.role!="professional":
            professNs.abort(401,"Unauthorized",errors={"role":"You aren't authorized to access this resource"})
        pdata = db.session.query(ServiceRequest,Professional.fees).join(ServiceRequest.professional).filter(ServiceRequest.professional_id==current_user.professional_data.id).all()
        d = []
        for sreq,fee in pdata:
            d.append({
                "status":sreq.status,
                "daterecieve":sreq.dateofrequest,
                "date":sreq.dateofcompletion,
                "earning":(sreq.work_units * fee) if sreq.work_units else 0
            })
        return d,200

@professNs.route("/reviewstats")
class PStat2(Resource):
    @jwt_required()
    @professNs.marshal_list_with(pstat_model2)
    def get(self):
        """Get review related stats of professional"""
        if current_user.role!="professional":
            professNs.abort(401,"Unauthorized",errors={"role":"You aren't authorized to access this resource"})
        pdata = ProfessionalReview.query.filter_by(professional_id=current_user.professional_data.id).all()
        return pdata,200