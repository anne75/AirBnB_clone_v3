#!/usr/bin/python3
from models.base_model import BaseModel, Base, Table, Column, String
from sqlalchemy.orm import relationship, backref
import hashlib
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
        reviews = relationship("Review", backref="user",
                               cascade="all, delete, delete-orphan")
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
        value = kwargs.get("password", "")
#        kwargs["password"] = hashlib.md5(bytes(value.encode('utf-8')))
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        return self.__dict__.get('password', "")

    @password.setter
    def password(self, value):
        """
        hash the password

        Argument:
           value: password new value
        """
        b = bytes(value.encode("utf-8"))
        self.__dict__['password'] = hashlib.md5(b)
