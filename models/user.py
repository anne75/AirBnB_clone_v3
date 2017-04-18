#!/usr/bin/python3
from models.base_model import BaseModel, Base, Table, Column, String
from sqlalchemy.orm import relationship, backref
from os import getenv
"""
user module
    contains
        The User Class inherts from BaseModel, Base
"""


class User(BaseModel, Base):
    """
    User class
    """
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = "users"
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user",
                              cascade="all, delete, delete-orphan")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """
        initializes from BaseModel
        """
        super().__init__(*args, **kwargs)
