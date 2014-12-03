import unittest
import os
import tempfile
import app
import api
from random import randint

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()
        app.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])


class TestAPIEndpoints(unittest.TestCase):

    def testGetUser(self):
        email = "test@6953905.com"
        password = "password"
        self.assertEqual(api.get_user(email, password), 62)

    def testSignUp(self):
        user_type = "teacher"
        email = "test@"+str(randint(0,1000))+str(randint(1000,4000))+".com"
        password = "password"
        first_name = "Foo"
        last_name = "Bar"
        self.assertEqual(api.create_teacher_user(user_type, email, password, first_name, last_name),"Successfully Added!")

    def testAddCohort(self):
        name = "Test Class"
        teacher_id = 62
        self.assertEqual(api.add_new_cohort(name, teacher_id), 3)

    def testAddStudent(self):
        user_type = "student"
        first_name = "Jane"
        last_name = "Doe"
        self.assertEqual(api.create_student(user_type, first_name, last_name), 68)

if __name__ == '__main__':
    unittest.main()