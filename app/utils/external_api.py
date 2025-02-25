import requests
from fastapi import status
from app.core.exceptions import InvalidCurrencyException
import os

API_KEY = os.getenv("API_APILAYER")


def get_currency(**kwargs):
    headers = {"apikey": API_KEY}
    if len(kwargs) > 2:
        response = requests.get(f"https://api.apilayer.com/currency_data/convert?to={kwargs['currency_from']}&from={kwargs['currency_to']}&amount={kwargs['amount']}",
                                headers=headers)
    elif len(kwargs) == 1:
        response = requests.get(
            f"https://api.apilayer.com/currency_data/live?source={kwargs['currency']}",
            headers=headers)
    else:
        response = requests.get(f"https://api.apilayer.com/currency_data/list",
                                headers=headers)
    if not response.json()['success']:
        raise InvalidCurrencyException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                        detail="Invalid currency was put")
    return response.json()
