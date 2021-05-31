# tests/test_basic.py
import unittest
import uuid
from math import ceil
from random import uniform

from src.utils.general import Struct
from test.common.Basecase import BaseTestCase
from cardvalidator import luhn


def roundUp(n, d=8):
    d = int('1' + ('0' * d))
    return ceil(n * d) / d

class FlaskTestCase(BaseTestCase):
    def setUp(self):
        self.testSetUp()

    def tearDown(self):
        self.testTearDown()

    def test_process_visa_card(self):
        with self.client:
            name = self.fake.name()
            post_data = {
                'merchant_identifier': str(uuid.uuid4()),
                "name": name,
                "credit_card_company": "visa",
                "credit_card_expiration_date": '02/26',
                "credit_card_cvv": self.fake.credit_card_security_code(),
                "credit_card_number": luhn.generate(16),
                "amount": roundUp(uniform(5.0, 100.9), 2),
            }
            headers = {}
            response = self.request_post('api/charge', headers, post_data)
            if response.status_code == 400:
                self.process_failed(response)
                return None
            self.process_success(response)

    def test_transction_list(self):
        with self.client:
            merchant_identifier = str(uuid.uuid4())
            for x in range(10):
                name = self.fake.name()
                post_data = {
                    'merchant_identifier': merchant_identifier,
                    "name": name,
                    "credit_card_company": "visa",
                    "credit_card_expiration_date": '02/26',
                    "credit_card_cvv": self.fake.credit_card_security_code(),
                    "credit_card_number": luhn.generate(16),
                    "amount": roundUp(uniform(5.0, 100.9), 2),
                }
                headers = {}
                self.request_post('api/charge', headers, post_data)

            response = self.request_get('/api/transactions/%s' % merchant_identifier, headers)
            self.assert200(response)
            data = Struct(response.json)
            self.assertTrue(data.status)
            print(data)

if __name__ == '__main__':
    unittest.main()
