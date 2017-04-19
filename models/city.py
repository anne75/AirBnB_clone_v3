#!/usr/bin/python3
from models.base_model import BaseModel, Base, Table, Column, String
from os import getenv
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
"""
city module
    contains
        the City class inherts from BaseModel, Base
"""


class City(BaseModel, Base):
    """
    The City class
    """
    if getenv('HBNB_TYPE_STORAGE', 'fs') == 'db':
        __tablename__ = 'cities'
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        name = Column(String(128), nullable=False)
        places = relationship("Place", backref="city",
                              cascade="all, delete, delete-orphan")
    else:
        name = ""
        state_id = ""

    def __init__(self, *args, **kwargs):
        """
        Initializes from BaseModel
        """
        super().__init__(*args, **kwargs)
