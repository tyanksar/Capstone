from app import create_app
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from models import setup_db, db, IT_Assets, Users, IT_Asset_Inventory
from unittest.mock import patch

'''
Below "mock_decorator" is to mimic a fake JWT token to
bybass the @requires_auth decorator in order to test the
endpoints without having to go through the
authentication process. To test the authentication with
associated roles please use Postman and import the file:
"fsnd-capstone-prod.postman_collection.json" to test the
roles in production or
"fsnd-capstone-dev.postman_collection.json" to test the
roles in development.
'''


def mock_decorator(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = 'fake'
            try:
                payload = 'fake'
            except:
                raise AuthError({
                    'code': 'invalid_claims',
                    'description':
                    'Incorrect claims. Please, check the audience and issuer.'
                }, 401)
            # check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator


patch('app.requires_auth', mock_decorator).start()


class CapstoneTestCase(unittest.TestCase):
    """This class represents the Capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres://{}/{}".format(
            'postgres@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Performing tests on each endpoint.
    """

    def test_01_add_it_assets(self):
        '''
        Successfuly adding an IT asset with the
        following attributes:
        "physical_id": "C123456"
        "type": "Computer"
        "status": PROD
        '''
        res = self.client().post('/assets',
                                 json={'physical_id': 'C123456',
                                       'type': 'Computer',
                                       'status': 'PROD'})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['it_asset'])

    def test_02_422_add_it_asset(self):
        '''
        Attempting to add an IT asset with the
        following attributes:
        "physical_id": "C123456"
        "type": "Computer"
        "status": None
        In which it should return a 422 error since
        the column "status" is not nullable.
        '''
        res = self.client().post('/assets',
                                 json={'physical_id': 'C999999',
                                       'type': 'Computer',
                                       'status': None})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable Entity")
        self.assertEqual(data['error'], 422)

    def test_03_patch_it_asset(self):
        '''
        Successfuly updating the "status" of the
        computer with "physical_id": "C123456" from
        "PROD" to "RTIP"
        '''
        res = self.client().patch('/assets/C123456',
                                  json={'physical_id': 'C123456',
                                        'type': 'Computer',
                                        'status': 'RTIP'})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_04_422_patch_it_asset(self):
        '''
        Attempting to update the "status" of the
        computer with "physical_id": "C123456" from
        "RTIP" to None in which it should return a
        422 error since "status" is not nullable
        '''
        res = self.client().patch('/assets/C123456',
                                  json={'physical_id': 'C123456',
                                        'type': 'Computer',
                                        'status': None})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable Entity")
        self.assertEqual(data['error'], 422)

    def test_05_get_it_assets(self):
        # successfuly retrieving all IT assets from the database.
        res = self.client().get('/assets')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['it_assets'])

    def test_06_add_user(self):
        '''
        Successfuly adding an usr with the
        following attributes:
        "name": "fake user"
        "badge_no": "111111"
        '''
        res = self.client().post('/users',
                                 json={'name': 'fake name',
                                       'badge_no': '111111', })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_07_422_add_user(self):
        '''
        Attempting to add a user with the
        following attributes:
        "name": None
        "badge_no": "222222"
        In which it should return a 422 error since
        the column "name" is not nullable.
        '''
        res = self.client().post('/users',
                                 json={'name': None,
                                       'badge_no': '222222'})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable Entity")
        self.assertEqual(data['error'], 422)

    def test_08_patch_user(self):
        '''
        Successfuly updating the "name" of the
        user with "badge_no": 111111 from
        "fake user" to "anothr fake user"
        '''
        res = self.client().patch('/users/111111',
                                  json={'name': 'another fake user'})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_09_422_patch_user(self):
        '''
        Attempting to update the "name" of the
        user with "badge_no": 111111 from
        "another fake user" to None in which it should return a
        422 error since "name" is not nullable
        '''
        res = self.client().patch('/users/111111', json={'name': None})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable Entity")
        self.assertEqual(data['error'], 422)

    def test_10_get_users(self):
        # successfuly retrieving all users from the database.
        res = self.client().get('/users')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_11_add_it_asset_inventory(self):
        # Successfuly adding an IT asset inventory
        res = self.client().post('/inventory',
                                 json={'physical_id': 'C123456',
                                       'badge_no': '111111'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_12_get_it_asset_inventory(self):
        # successfuly retrieving all IT assets from the database.
        res = self.client().get('/inventory')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['it_asset_inventory'])

    def test_13_delete_it_assets(self):
        # Successfuly deleting an IT asset with physical ID: "C123456"
        res = self.client().delete('/assets/C123456')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_14_404_delete_it_assets(self):
        '''
        Attempting to delete an IT asset with
        physical ID: "C99999" in which it should
        return a 404 error since the IT asset does
        not exist in the database
        '''
        res = self.client().delete('/assets/C99999')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not Found")
        self.assertEqual(data['error'], 404)

    def test_15_delete_user(self):
        # Successfuly deleting a user with badge no.: 111111
        res = self.client().delete('/users/111111')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_16_404_delete_user(self):
        '''
        Attempting to delete a user with
        badge no.: 999999 in which it should
        return a 404 error since the user does
        not exist in the database
        '''
        res = self.client().delete('/users/999999')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not Found")
        self.assertEqual(data['error'], 404)

    def test_17_404_add_it_asset_inventory(self):
        '''
        Attempting to add an it asset inventory record
        where a phyisial ID or a badge no. does not
        exist in which it should return a 404 error since
        there are no records in the database
        '''
        res = self.client().post('/inventory',
                                 json={'physical_id': 'C123456',
                                       'badge_no': '111111'})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not Found")
        self.assertEqual(data['error'], 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
