import unittest
from flask import current_app
from app import create_app, db
<<<<<<< HEAD
=======
from app.models import User
>>>>>>> more-temp


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
<<<<<<< HEAD
=======
        

class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
    u = User(password = 'cat')
    self.assertTrue(u.password_hash is not None)

def test_no_password_getter(self):
    u = User(password = 'cat')
    with self.assertRaises(AttributeError):
        u.password

def test_password_verification(self):
    u = User(password = 'cat')
    self.assertTrue(u.verify_password('cat'))
    self.assertFalse(u.verify_password('dog'))

def test_password_salts_are_random(self):
    u = User(password='cat')
    u2 = User(password='cat')
    self.assertTrue(u.password_hash != u2.password_hash)
>>>>>>> more-temp
