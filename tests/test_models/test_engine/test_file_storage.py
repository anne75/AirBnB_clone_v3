import unittest
import os
from datetime import datetime
from models.engine.file_storage import FileStorage
from models import *


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE', 'fs') == 'db',
                 "db does not have FileStorage")
class Test_FileStorage(unittest.TestCase):
    """
    Test the file storage class
    """

    def setUp(self):
        self.store = FileStorage()

        test_args = {'updated_at': datetime(2017, 2, 12, 00, 31, 53, 331997),
                     'id': 'f519fb40-1f5c-458b-945c-2ee8eaaf4900',
                     'created_at': datetime(2017, 2, 12, 00, 31, 53, 331900)}
        self.model = BaseModel(test_args)

        self.test_len = len(self.store.all())

#    @classmethod
#    def tearDownClass(cls):
#        import os
#        if os.path.isfile("test_file.json"):
#            os.remove('test_file.json')

    def test_all(self):
        self.assertEqual(len(self.store.all()), self.test_len)

    def test_new(self):
        # note: we cannot assume order of test is order written
        test_len = len(self.store.all())
        # self.assertEqual(len(self.store.all()), self.test_len)
        new_obj = State()
        new_obj.save()
        self.assertEqual(len(self.store.all()), test_len + 1)
        a = BaseModel()
        a.save()
        self.assertEqual(len(self.store.all()), self.test_len + 2)

    def test_save(self):
        self.test_len = len(self.store.all())
        a = BaseModel()
        a.save()
        self.assertEqual(len(self.store.all()), self.test_len + 1)
        b = User()
        self.assertNotEqual(len(self.store.all()), self.test_len + 2)
        b.save()
        self.assertEqual(len(self.store.all()), self.test_len + 2)

    def test_reload(self):
        self.model.save()
        a = BaseModel()
        a.save()
        self.store.reload()
        for value in self.store.all().values():
            self.assertIsInstance(value.created_at, datetime)

    def test_state(self):
        """test State creation with an argument"""
        pass

if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(1, os.path.join(os.path.split(__file__)[0], '../../..'))
    from models import *
    from models.engine.file_storage import FileStorage
    unittest.main()
