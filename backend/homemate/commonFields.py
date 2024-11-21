from homemate import api
from flask_restx import fields

address_model = api.model("AddressModel",{
    "base_address":fields.String,
    "city":fields.String,
    "state":fields.String,
    "pincode":fields.String
})