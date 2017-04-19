#/usr/bin/python3
from flask import Blueprint
from models.city import City
from models import storage
from models.state import State
"""
creates the Blueprint for flask application
"""

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

#what is the point of this line?
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *

