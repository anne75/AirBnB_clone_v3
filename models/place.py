#!/usr/bin/python3
from models.base_model import BaseModel, Base, Table, Column
from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKey, String, Integer, Float
from os import getenv
"""
place module
    contains
        PlaceAmenity inherts from Base
            used to link table places and amenities
        Place inherts from BaseModel and Base
"""


class PlaceAmenity(Base):
    """
    PlaceAmenity class designed to link table places and table amenities
    of the SQLAlchmeny
    """
    if getenv('HBNB_TYPE_STORAGE', 'fs') == 'db':
        __tablename__ = "place_amenity"
        place_id = Column(String(60), ForeignKey('places.id'),
                          primary_key=True, nullable=False)
        amenity_id = Column(String(60), ForeignKey('amenities.id'),
                            primary_key=True, nullable=False)


class Place(BaseModel, Base):
    """
    Place Class
    """
    if getenv('HBNB_TYPE_STORAGE', 'fs') == 'db':
        __tablename__ = "places"
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        amenities = relationship("Amenity", secondary="place_amenity",
                                 viewonly=True)
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenities = []

    def __init__(self, *args, **kwargs):
        """
        initializes the Place Class instance
        Inherts from BaseClass
        """
        super().__init__(*args, **kwargs)
