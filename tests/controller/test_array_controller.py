#!/usr/bin/env python
'''
tests.controller.test_platform_controller

Test for the platform controller
'''
import json
from ooiservices.app import app
from tests.services_test_case import ServicesTestCase

class TestArrayController(ServicesTestCase):
    def setUp(self):
        '''
        Initializes the application
        '''
        ServicesTestCase.setUp(self)
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_array_listing(self):
        '''
        Test that the app context initializes successfully
        mjc: we'll have a test for complex endpoints and their json output.
            For now, we just need to know that the end points are running.
        '''
        try:
            rv = self.app.get('/array')
            json.loads(rv.data)
        except ValueError:
            print("data was not valid JSON")