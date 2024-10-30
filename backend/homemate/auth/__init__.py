from flask_restx import Namespace

authNamespace = Namespace("auth",description="Namespace for authentication, to get new JW tokens or refresh older one.")

import homemate.auth.views