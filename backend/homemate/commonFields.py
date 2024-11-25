from homemate import api
from flask_restx import fields

address_model = api.model("AddressModel",{
    "base_address":fields.String,
    "city":fields.String,
    "state":fields.String,
    "pincode":fields.String
})

User_model = api.model("User_model",{
    "id":fields.Integer,
    "username":fields.String,
    "email_address":fields.String,
    "role":fields.String,
    "date_joined":fields.Date
})