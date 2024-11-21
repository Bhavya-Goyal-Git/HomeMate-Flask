from flask_restx import Namespace

professNs = Namespace("professional",description="Namespace for professionals' related requests.")

import homemate.professional.views