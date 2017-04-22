#!/usr/bin/python3
"""
Testing app.py file
"""
import flask
print("HERE")
# import flaskr
print("HERE")
import unittest
print("HERE")
from models import storage
print("HERE")
from api.v1.app import app
print("HERE")



class TestApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_404(self):
        rv = self.app.get('/bad')
        print(rv.data)
            # self.assertIn("Not found", flask.request.data)



if __name__ == "__main__":
    unittest.main()
