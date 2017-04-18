import unittest
import os
from datetime import datetime
from models import *
from models.place import PlaceAmenity


class Test_PlaceModel(unittest.TestCase):
    """
    Test the place model class
    """

    def test_simple_initialization(self):
        """initialization without arguments"""
        model = Place()
        self.assertTrue(hasattr(model, "id"))
        self.assertTrue(hasattr(model, "created_at"))
        self.assertTrue(hasattr(model, "city_id"))
        self.assertTrue(hasattr(model, "user_id"))
        self.assertTrue(hasattr(model, "name"))
        self.assertTrue(hasattr(model, "description"))
        self.assertTrue(hasattr(model, "number_rooms"))
        self.assertTrue(hasattr(model, "number_bathrooms"))
        self.assertTrue(hasattr(model, "max_guest"))
        self.assertTrue(hasattr(model, "price_by_night"))
        self.assertTrue(hasattr(model, "latitude"))
        self.assertTrue(hasattr(model, "longitude"))

    def test_var_initialization(self):
        """Check default type"""
        model = Place()
        self.assertIsInstance(model.created_at, datetime)

    def test_save(self):
        """saving the object to storage"""
        test_user = {'id': "001",
                     'email': "you@g.com",
                     'password': "1234",
                     'first_name': "TEST",
                     'last_name': "REVIEW"}
        user = User(test_user)
        test_state = {'id': "002",
                      'created_at': datetime(2017, 2, 12, 00, 31, 55, 331997),
                      'name': "TEST STATE FOR CITY"}
        state = State(test_state)
        test_city = {'id': "003",
                     'name': "CITY SET UP",
                     'state_id': "002"}
        city = City(test_city)
        test_place = {'id': "003",
                      'city_id': "003",
                      'user_id': "001",
                      'name': "TEST REVIEW",
                      'description': "blah blah",
                      'number_rooms': 4,
                      'number_bathrooms': 2,
                      'max_guest': 4,
                      'price_by_night': 23,
                      'latitude': 45.5,
                      'longitude': 23.4}
        place = Place(test_place)
        user.save()
        state.save()
        city.save()
        place.save()
        storage.delete(place)
        # storage.delete(city) # cascade deletes it
        storage.delete(user)
        storage.delete(state)


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE', 'fs') != 'db', "db")
class Test_PlaceAmenityModel(unittest.TestCase):
    """
    Test the place amenity model class
    """

    def test_save(self):
        """creates and save a PlaceAmenity object"""
        test_user = {'id': "002",
                     'email': "you@g.com",
                     'password': "1234",
                     'first_name': "TEST",
                     'last_name': "REVIEW"}
        user = User(**test_user)
        test_state = {'id': "001",
                      'created_at': datetime(2017, 2, 12, 00, 31, 55, 331997),
                      'name': "TEST STATE FOR CITY"}
        state = State(**test_state)
        test_city = {'id': "005",
                     'name': "CITY SET UP",
                     'state_id': "001"}
        city = City(**test_city)
        test_place = {'id': "002",
                      'city_id': "005",
                      'user_id': "002",
                      'name': "TEST REVIEW",
                      'description': "blah blah",
                      'number_rooms': 4,
                      'number_bathrooms': 2,
                      'max_guest': 4,
                      'price_by_night': 23,
                      'latitude': 45.5,
                      'longitude': 23.4}
        place = Place(**test_place)
        test_amenity = {'id': "010",
                        'name': "TEST place_amenities"}
        amenity = Amenity(**test_amenity)
        pla = PlaceAmenity(place_id="002", amenity_id="010")
        user.save()
        state.save()
        city.save()
        place.save()
        amenity.save()
        storage._DBStorage__session.add(pla)
        tmp = storage._DBStorage__session.query(PlaceAmenity).one()
        storage._DBStorage__session.delete(tmp)
        # storage.delete(amenity) ???, foreign key constraint on empty set
        # storage.delete(place)
        # storage.delete(user)
        # storage.delete(state)


if __name__ == "__main__":
    unittest.main()
