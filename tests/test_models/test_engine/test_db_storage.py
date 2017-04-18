from datetime import datetime
from models import *
from models.amenity import Amenity
from models.base_model import Base
from models.engine.db_storage import DBStorage
from models.state import State
import os.path
from os import getenv
import unittest


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE', 'fs') != 'db', "db")
class Test_DBStorage(unittest.TestCase):
    """
    Test the file storage class
    """
    @classmethod
    def setUpClass(cls):
        """create a session"""
        # close previous connexion to same database
        storage._DBStorage__session.close()
        cls.store = DBStorage()
        test_args = {'updated_at': datetime(2017, 2, 12, 00, 31, 53, 331997),
                     'id': "0234",
                     'created_at': datetime(2017, 2, 12, 00, 31, 53, 331900),
                     'name': 'wifi'}
        cls.model = Amenity(**test_args)
        cls.store.reload()
        cls.test_len = 0

    @classmethod
    def tearDownClass(cls):
        cls.store._DBStorage__session.close()
        storage.reload()

    def test_all(self):
        output = self.store.all('Amenity')
        self.assertEqual(len(output), self.test_len)

    def test_new(self):
        # note: we cannot assume order of test is order written
        self.test_len = len(self.store.all())
        # self.assertEqual(len(self.store.all()), self.test_len)
        self.model.save()
        self.store.reload()
        self.assertEqual(len(self.store.all()), self.test_len + 1)
        a = Amenity(name="thing")
        a.save()
        self.store.reload()
        self.assertEqual(len(self.store.all()), self.test_len + 2)

    def test_save(self):
        test_len = len(self.store.all())
        a = Amenity(name="another")
        a.save()
        self.store.reload()
        self.assertEqual(len(self.store.all()), test_len + 1)
        b = State(name="california")
        self.assertNotEqual(len(self.store.all()), test_len + 2)
        b.save()
        self.store.reload()
        self.assertEqual(len(self.store.all()), test_len + 2)

    def test_reload(self):
        self.model.save()
        a = Amenity(name="different")
        a.save()
        self.store.reload()
        for value in self.store.all().values():
            self.assertIsInstance(value.created_at, datetime)

    def test_state(self):
        """test State creation with an argument"""
        a = State(name="Kamchatka", id="Kamchatka666")
        a.save()
        self.store.reload()
        self.assertIn("Kamchatka666", self.store.all("State").keys())

    def test_count(self):
        """test count all"""
        test_len = len(self.store.all())
        a = Amenity(name="test_amenity")
        a.save()
        self.store.reload()
        self.assertEqual(test_len + 1, self.store.count())

    def test_count_arg(self):
        """test count with an argument"""
        test_len = len(self.store.all("Amenity"))
        a = Amenity(name="test_amenity_2")
        a.save()
        self.store.reload()
        self.assertEqual(test_len + 1, self.store.count("Amenity"))

    def test_count_bad_arg(self):
        """test count with dummy class name"""
        self.assertEqual(-1, self.store.count("Dummy"))

    def test_get(self):
        """test get with valid cls and id"""
        a = Amenity(name="test_amenity3", id="test_3")
        a.save()
        self.store.reload()
        result = self.store.get("Amenity", "test_3")
        self.assertEqual(a.name, result.name)
        # does not work as the database loses last argument tzinfo for datetime
        # self.assertEqual(a.created_at, result.created_at)
        self.assertEqual(a.created_at.year, result.created_at.year)
        self.assertEqual(a.created_at.month, result.created_at.month)
        self.assertEqual(a.created_at.day, result.created_at.day)
        self.assertEqual(a.created_at.hour, result.created_at.hour)
        self.assertEqual(a.created_at.minute, result.created_at.minute)
        self.assertEqual(a.created_at.second, result.created_at.second)

    def test_get_bad_cls(self):
        """test get with invalid cls"""
        result = self.store.get("Dummy", "test")
        self.assertIsNone(result)

    def test_get_bad_id(self):
        """test get with invalid id"""
        result = self.store.get("State", "very_bad_id")
        self.assertIsNone(result)


if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(1, os.path.join(os.path.split(__file__)[0], '../../..'))
    from models import *
    from models.engine.file_storage import FileStorage
    unittest.main()
