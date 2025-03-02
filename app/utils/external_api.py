from fastapi import status
from app.core.exceptions import InvalidCurrencyException
import os
import httpx

API_KEY = os.getenv("API_APILAYER")


async def get_currency(**kwargs) -> dict:
    headers = {"apikey": API_KEY}
    async with httpx.AsyncClient() as client:
        if len(kwargs) > 2:
            url = f"https://api.apilayer.com/currency_data/convert?to={kwargs['currency_from']}&from={kwargs['currency_to']}&amount={kwargs['amount']}"
        elif len(kwargs) == 1:
            url = f"https://api.apilayer.com/currency_data/live?source={kwargs['currency']}"
        else:
            url = f"https://api.apilayer.com/currency_data/list"
        response = await client.get(url, headers=headers)
        if not response.json()['success']:
            raise InvalidCurrencyException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                            detail="Given currency has invalid syntaxis. Try again")
    return response.json()
