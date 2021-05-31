import os
from time import sleep

from sqlalchemy import func

from config import settings
from config.database import db
from src.models import BadRecord
from src.utils.common_methods import request_post
from src.utils.enums import CreditType

from src.utils.responses import response_error, response_success


class ProcessingService():
    processor_retry = None
    number_of_retry = 1

    def switcher_by_type_card(self, card_type, card_data):
        switcher = {
            CreditType.Visa: self.processor_visa,
            CreditType.MasterCard: self.processor_mastercard,
        }

        func = switcher.get(card_type, lambda: 'Invalid')
        return func(card_data)

    def processor(self, card_type, card_data):
        self.processor_retry = None
        return self.switcher_by_type_card(card_type, card_data)

    def processor_retry(self, processor_retry, card_type, card_data):
        self.processor_retry = processor_retry
        return self.switcher_by_type_card(card_type, card_data)

    def processor_visa(self, card_data):
        name_arr = card_data.name.split(' ')
        post_data = {
            'fullName': card_data.name,
            'expiration': card_data.credit_card_expiration_date,
            'cvv': card_data.credit_card_cvv,
            'number': card_data.credit_card_number,
            'totalAmount': card_data.amount
        }
        data = request_post(settings[os.environ.get("FLASK_ENV", "development")].REQUEST_VISA_API, {
            "identifier": name_arr[0]
        }, post_data)
        if self.processor_retry is not None and \
                data is None and \
                self.number_of_retry >= settings[os.environ.get("FLASK_ENV", "development")].MAX_NUMBER_OF_RETRY:
            self.number_of_retry = self.number_of_retry + 1
            sleep(self.processor_retry)
            return self.processor_visa(card_data)

        reason = ''
        if data['chargeResult'].lower() == 'failure':
            reason = data['resultReason'].lower()
        return self.handle_processor_response(data, card_data.merchant_identifier, CreditType.Visa,
                                              card_data.name, card_data.amount, reason)

    def processor_mastercard(self, card_data):
        name_arr = card_data.name.split(' ')
        post_data = {
            'first_name': name_arr[0],
            'last_name': name_arr[1],
            'expiration': card_data.credit_card_expiration_date,
            'cvv': card_data.credit_card_cvv,
            'card_number': card_data.credit_card_number,
            'charge_amount': card_data.amount
        }
        data = request_post(settings[os.environ.get("FLASK_ENV", "development")].REQUEST_MASTERCARD_API, {
            "identifier": name_arr[0]
        }, post_data)
        if self.processor_retry is not None and \
                data is None and \
                self.number_of_retry >= settings[os.environ.get("FLASK_ENV", "development")].MAX_NUMBER_OF_RETRY:
            self.number_of_retry = self.number_of_retry + 1
            sleep(self.processor_retry)
            return self.processor_mastercard(card_data)
        reason = ''
        if 'error' in data:
            reason = data['error'].lower()
        if 'decline_reason' in data:
            reason = data['decline_reason'].lower()
        return self.handle_processor_response(data, card_data.merchant_identifier, CreditType.MasterCard,
                                              card_data.name, card_data.amount, reason)

    def record_bad_charge(self, merchant_identifier, card_type, full_name, amount, result_reason):
        record = BadRecord(merchant_identifier, card_type.value, result_reason, full_name, amount)
        db.session.add(record)
        db.session.commit()

    def handle_processor_response(self, data, merchant_identifier, card_type, full_name, amount, result_reason=''):
        if data is None:
            return response_error("Error on processor", {
                'errors': 'processor Failed please contact support'
            }, 500)
        if result_reason != '':
            self.record_bad_charge(merchant_identifier, card_type, full_name, amount, result_reason)
            return response_error("Error on processor", {
                'reason': result_reason,
                'errors': 'insufficient funds'
            }, 400)
        return response_success({"process": "OK"})

    def get_transactions_count(self, merchant_identifier):
        records = BadRecord.query.with_entities(
            BadRecord.reason,
            BadRecord.fullname,
            BadRecord.card_type,
            BadRecord.amount,
            BadRecord.created_at,
            func.count(BadRecord.id)).filter_by(merchant_identifier=merchant_identifier).group_by(
            BadRecord.reason).all()
        data = []
        for r in records:
            data.append(r._asdict())
        return data
