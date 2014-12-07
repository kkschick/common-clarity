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

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])

    def testIndexPage(self):
        response = self.app.get("/")
        self.assertIn("CommonClarity", response.data)

class TestAPIEndpoints(unittest.TestCase):

    def testGetUser(self):
        email = "test@1182442.com"
        password = "password"
        self.assertEqual(api.get_user(email, password), 84)

    def testGetUserFail(self):
        email = "safs@adjslfda.com"
        password = "laksjfdfsafsdf"
        self.assertEqual(api.get_user(email, password), "User does not exist.")

    def testSignUp(self):
        user_type = "teacher"
        email = "test@"+str(randint(0,1000))+str(randint(1000,4000))+".com"
        password = "password"
        first_name = "Foo"
        last_name = "Bar"
        self.assertEqual(api.create_teacher_user(user_type, email, password, first_name, last_name),"Successfully Added!")

    def testAddCohort(self):
        name = "TestClass"
        teacher_id = 85
        self.assertEqual(api.add_new_cohort(name, teacher_id), 7)

    def testAddStudent(self):
        user_type = "student"
        first_name = "John"
        last_name = "Smith"
        self.assertEqual(api.create_student(user_type, first_name, last_name), 87)

    def testAddStudentToCohort(self):
        student_id = 87
        cohort_id = 7
        self.assertEqual(api.add_student_to_cohort(student_id, cohort_id), "Successfully Added!")

    def testGetTeacherCohorts(self):
        teacher_id = 84
        cohorts = [{'cohort_id': 6, 'students': [{'name': u'Jane Doe', 'id': 86}], 'name': u'Test Class'}]
        self.assertEqual(api.get_teacher_cohorts(teacher_id), cohorts)

if __name__ == '__main__':
    unittest.main()