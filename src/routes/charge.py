import os

from flask import request
from marshmallow import ValidationError

from config import settings
from config.api import app as current_app
from src.schemas.requests.charge import RequestChargePayment
from src.services.ProcceingService import ProcessingService
from src.utils.enums import CreditType
from src.utils.general import Struct
from src.utils.responses import response_success, response_error

processingService = ProcessingService()


@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/charge"),
                   methods=['POST'])
def charge_payment():
    if not request.is_json:
        return response_error("request body not in json format", {'params': request.data}, 400)
    try:
        schema = RequestChargePayment()
        data = schema.load(request.json)
    except ValidationError as e:
        return response_error("Error on format of the params", {'params': request.json, 'errors': e.messages}, 400)
    body = Struct(data)
    card_type = CreditType(body.credit_card_company.lower())
    return processingService.processor(card_type, body)


@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(
    route="/charge/<wait_per_retry>/retry"),
    methods=['POST'])
def retry_charge_payment(wait_per_retry):
    if not request.is_json:
        return response_error("request body not in json format", {'params': request.data}, 400)
    try:
        schema = RequestChargePayment()
        data = schema.load(request.json)
    except ValidationError as e:
        return response_error("Error on format of the params", {'params': request.json, 'errors': e.messages}, 400)
    body = Struct(data)
    card_type = CreditType(body.credit_card_company.lower())
    return processingService.processor_retry(wait_per_retry, card_type, body)


@current_app.route(
    settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(
        route="/transactions/<merchant_idenentify>"))
def get_merchant_transactions(merchant_idenentify):
    data = processingService.get_transactions_count(merchant_idenentify)
    return response_success(data)

