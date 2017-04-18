import unittest
import os
from datetime import datetime
from models import *


class Test_CityModel(unittest.TestCase):
    """
    Test the city model class
    """

    def test_save(self):
        """Set up the variables before the test"""
        test_state = {'updated_at': datetime(2017, 2, 12, 00, 31, 50, 331997),
                      'id': "001",
                      'created_at': datetime(2017, 2, 12, 00, 31, 55, 331997),
                      'name': "TEST STATE FOR CITY"}
        state = State(test_state)
        state.save()
        test_args = {'updated_at': datetime(2017, 2, 12, 00, 31, 53, 331997),
                     'id': 'f519fb40-1f5c-458b-945c-2ee8eaaf4900',
                     'created_at': datetime(2017, 2, 12, 00, 31, 53, 331900),
                     'name': "CITY SET UP",
                     'state_id': "001"}
        model = City(test_args)
        model.save()
        storage.delete(model)
        storage.delete(state)

    def test_var_initialization(self):
        """test simple initialization"""
        test_args = {'updated_at': datetime(2017, 2, 12, 00, 31, 53, 331997),
                     'id': 'f519fb40-1f5c-458b-945c-2ee8eaaf4900',
                     'created_at': datetime(2017, 2, 12, 00, 31, 53, 331900),
                     'name': "CITY SET UP",
                     'state_id': "001"}
        model = City(test_args)
        self.assertTrue(hasattr(model, "name"))
        self.assertTrue(hasattr(model, "state_id"))
        self.assertEqual(model.name, "CITY SET UP")
        self.assertEqual(model.state_id, "001")

    def test_initialization_no_arg(self):
        """test initialization without arguments"""
        new = City()
        self.assertTrue(hasattr(new, "name"))
        self.assertTrue(hasattr(new, "state_id"))
        self.assertTrue(hasattr(new, "created_at"))
        self.assertIsInstance(new.created_at, datetime)


if __name__ == "__main__":
    unittest.main()
