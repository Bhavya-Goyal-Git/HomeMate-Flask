from homemate.professional import professNs
from homemate import app
from flask_restx import Resource, reqparse, fields
from flask_jwt_extended import jwt_required, current_user
from ..models import db
from ..models.tables import Professional
import homemate.validators as validator
from ..commonFields import address_model
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import os

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
    "isverified":fields.Boolean,
    "experience":fields.Integer,
    "rating":fields.Integer,
    "num_raters":fields.Integer,
    "service_id":fields.Integer,
    "fees":fields.Float,
    "fees_unit":fields.String,
})

@professNs.route("/data/<int:id>")
class ProfessionalData(Resource):
    
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
        fname = secure_filename(doc_file.filename)
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
        except:
            db.session.rollback()
            professNs.abort(404,"Some error occured",errors={"database":"Database error occured"})
        return newprofessional.to_dict(),201