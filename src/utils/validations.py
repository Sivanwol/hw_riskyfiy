import pycountry
from cardvalidator import formatter


def valid_currency(currency):
    try:
        pycountry.currencies.lookup(currency.upper())
    except LookupError:
        return False
    return True


def allow_card_types(credit_number):
    return formatter.is_visa(credit_number) or \
           formatter.is_mastercard(credit_number)
