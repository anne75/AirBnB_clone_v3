#!/usr/bin/python3
from models.base_model import BaseModel, Base, Table, Column, String
from os import getenv
"""
amenity module
    contains
        the Amentiry class inherts from BaseModel and Base
"""


class Amenity(BaseModel, Base):
    """
    The Amenity class
    """
    if getenv('HBNB_TYPE_STORAGE', 'fs') == 'db':
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """
        initializes class objects. Inherts attributes from parent
        """
        super().__init__(*args, **kwargs)
