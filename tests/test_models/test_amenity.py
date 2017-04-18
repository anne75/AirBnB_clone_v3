import unittest
import os
from datetime import datetime
from models import *


class Test_AmenityModel(unittest.TestCase):
    """
    Test the amenity model class
    """

    def test_save(self):
        """set up before running any test"""
        test_args = {'updated_at': datetime(2017, 2, 12, 00, 31, 53, 331997),
                     'id': '054',
                     'created_at': datetime(2017, 2, 12, 00, 31, 53, 331900),
                     'name': "AMENITY SET UP"}
        model = Amenity(**test_args)
        model.save()
        storage.delete(model)

    def test_var_initialization(self):
        """test the creation of the model went right"""
        test_args = {'updated_at': datetime(2017, 2, 12, 00, 31, 53, 331997),
                     'id': '055',
                     'created_at': datetime(2017, 2, 12, 00, 31, 53, 331900),
                     'name': "AMENITY SET UP"}
        model = Amenity(**test_args)
        self.assertEqual(model.name, "AMENITY SET UP")

    def test_missing_arg(self):
        """test creating an Amenity with no argument"""
        new = Amenity()
        self.assertTrue(hasattr(new, "id"))
        self.assertTrue(hasattr(new, "name"))

    def test_date_format(self):
        """test the date has the right type"""
        model = Amenity()
        self.assertIsInstance(model.created_at, datetime)


if __name__ == "__main__":
    unittest.main()
