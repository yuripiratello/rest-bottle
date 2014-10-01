# coding: utf-8
import unittest
from webtest import TestApp
import run

test_app = TestApp(run.app)


class TestAddPerson(unittest.TestCase):
    def test_add_person_parameter_not_found(self):
        response = test_app.post('/person', status=404)
        self.assertEqual(response.status_int, 404)

    def test_add_invalid_person(self):
        response = test_app.post('/person', {
            'facebookId': 75456456
        }, status=412)
        self.assertEqual(response.status_int, 412)

    def test_add_person(self):
        response = test_app.post('/person', {
            'facebookId': 100000523240928
        }, status=201)
        self.assertEqual(response.status_int, 201)

    def test_add_person_exists(self):
        response = test_app.post('/person', {
            'facebookId': 100000523240928
        }, status=409)
        self.assertEqual(response.status_int, 409)


class TestGetPerson(unittest.TestCase):
    def test_get_person(self):
        response = test_app.get(
            '/person/?facebookId=100001885167982', status=404)
        self.assertEqual(response.status_int, 404)

        response = test_app.post('/person', {
            'facebookId': 100001885167982
        }, status=201)
        self.assertEqual(response.status_int, 201)

        response = test_app.get('/person/')
        self.assertEqual(response.status_int, 200)
        self.assertEqual(len(response.json), 2)

        response = test_app.get('/person/?limit=1')
        self.assertEqual(response.status_int, 200)
        self.assertEqual(len(response.json), 1)

        response = test_app.get('/person/?facebookId=100001885167982')
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json['facebook_id'], 100001885167982)


# If running this file, run the tests
# invoke with `python -m unittest discover`
if __name__ == '__main__':
    unittest.main()