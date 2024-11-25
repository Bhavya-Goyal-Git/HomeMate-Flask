from flask_restx import Namespace

serviceNs = Namespace("service",description="Namespace for Services")

import homemate.services.views