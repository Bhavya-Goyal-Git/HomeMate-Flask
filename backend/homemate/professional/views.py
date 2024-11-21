from homemate.professional import professNs
from flask_restx import Resource, reqparse, fields
from flask_jwt_extended import jwt_required, current_user
from ..models import db
from ..models.tables import Professional
import homemate.validators as validator
from ..commonFields import address_model