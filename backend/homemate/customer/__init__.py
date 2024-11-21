from flask_restx import Namespace

customerNs = Namespace("customer",description="Namespace for customer related requests.")

import homemate.customer.views