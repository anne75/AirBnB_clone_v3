#/usr/bin/python3
"""
creates the Blueprint for flask application
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

#what is the point of this line?
from api.v1.views.index import *
