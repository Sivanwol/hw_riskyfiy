from marshmallow import Schema, fields, validates_schema, ValidationError, validate
from cardvalidator import luhn


class RequestChargePayment(Schema):
    merchant_identifier = fields.Str(required=True, validate=validate.Length(
        min=3,
        max=100,
        error='field merchant_identifier not valid'))
    name = fields.Str(required=True, validate=validate.Length(min=3, max=100, error='field name not valid'))
    credit_card_company = fields.Str(required=True, validate=validate.Length(max=50, error='field company not valid'))
    credit_card_expiration_date = fields.Str(required=True, validate=validate.Length(
        max=5,
        error='field credit_card_expiration_date not valid'))
    credit_card_cvv = fields.Str(required=True,
                                 validate=validate.Length(max=5, error='field credit_card_cvv not valid'))
    credit_card_number = fields.Str(required=True)
    amount = fields.Float()

    @validates_schema
    def validate_credit_card(self, data, **kwargs):
        errors = {}
        if not luhn.is_valid(data['credit_card_number']):
            errors["credit_card_number"] = ["field credit_card_number is not credit card number"]
        if data['amount'] <= 0:
            errors["amount"] = ["field amount not allow 0 or lower"]
        if errors:
            raise ValidationError(errors)
