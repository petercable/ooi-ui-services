#!/usr/bin/env python
'''
Tests system utilities.

'''
__author__ = "Jim Case"

import unittest
import json
from base64 import b64encode
from flask import url_for
from ooiservices.app import create_app, db, cache
from ooiservices.app.models import User, UserScope, Organization

test_username = 'admin'
test_password = 'test'


class SystemTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TESTING_CONFIG')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=False)
        Organization.insert_org()
        User.insert_user(username=test_username, password=test_password)
        UserScope.insert_scopes()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self, username, password):
        return {
            'Authorization': 'Basic ' + b64encode(
                (username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_list_routes(self):
        # Get routes
        response = self.client.get(url_for('main.list_routes'),
                                   content_type='application/json')
        self.assertTrue(response.status_code == 200)

        data = json.loads(response.data)
        self.assertIn('routes', data)

    '''
    The redis cache clear route is defined by:
    '''
    def test_clear_redis(self):
        # setup a test cache list
        cache.set('test_list', [{'something': 'something'}, {'dark': 'side'}])

        # test GET
        response = self.client.get(url_for('main.cache_list'),
                                   content_type='application/json')

        self.assertTrue('test_list' in response)

        # test DELETE
        response = self.client.delete(url_for('main.cache_list')+'/test_list',
                                      content_type='application/json')

        self.assertTrue(1 in response)
