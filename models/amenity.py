#!/usr/bin/python3
from models.base_model import BaseModel, Base, Table, Column, String
from os import getenv
from sqlalchemy.orm import relationship, backref
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
#        amenities_place = relationship("Amenity", secondary="amenity",
#                                 viewonly=True,
#                                 cascade="all, delete, delete-orphan")
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """
        initializes class objects. Inherts attributes from parent
        """
        super().__init__(*args, **kwargs)
