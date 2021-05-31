import json
import os

from faker import Faker
from flask_testing import TestCase

from config.api import app
from config.database import db
from src.utils.general import Struct


class BaseTestCase(TestCase):
    """A base test case."""

    fake = Faker()
    TESTING = True

    def create_app(self):
        # app.config.from_object('config.TestConfig')
        print(os.environ.get("FLASK_ENV", "development"))
        app.app_context().push()
        return app

    def testSetUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        db.session.commit()
        self.init_unit_data()
        Faker.seed(0)

    def testTearDown(self):
        db.session.remove()
        db.drop_all()

    def init_unit_data(self):
        pass

    def process_failed(self, response):
        print("Failed Process")
        self.assert400(response)
        data = Struct(response.json)
        self.assertFalse(data.status)
        self.assertEqual(data.error, 'Error on processor')
        self.assertEqual(data.error_params.errors, 'insufficient funds')

    def process_success(self, response):
        print("success Process")
        self.assert200(response)
        data = Struct(response.json)
        self.assertTrue(data.status)
        self.assertEqual(data.data.process.lower(), 'ok')

    def request_get(self, url, headers):
        headers_defualt = {'Content-Type': 'application/json'}
        headers = headers_defualt | headers
        print('request get -> %s' % url)
        print('request headers -> %s' % json.dumps(headers))
        return self.client.get(
            url,
            headers=headers
        )

    def request_put(self, url, token, data={}):
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % token}
        print('request put -> %s' % url)
        print('request headers -> %s' % json.dumps(headers))
        print('request put data-> %s' % json.dumps(data))
        return self.client.put(
            url,
            data=json.dumps(data),
            headers=headers
        )

    def request_post(self, url, headers, data={}):
        headers_defualt = {'Content-Type': 'application/json'}
        headers = headers_defualt | headers
        print('request post -> %s' % url)
        print('request headers_defualt -> %s' % json.dumps(headers))
        print('request post data-> %s' % json.dumps(data))
        return self.client.post(
            url,
            data=json.dumps(data),
            headers=headers
        )

    def request_delete(self, url, token):
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % token}
        print('request delete -> %s' % url)
        print('request headers -> %s' % json.dumps(headers))
        return self.client.delete(
            url,
            headers=headers
        )
