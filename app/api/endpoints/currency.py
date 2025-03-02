from typing import Annotated
from fastapi import APIRouter, Depends, Query
from app.core.security import get_current_user
from dotenv import load_dotenv
from app.utils.external_api import get_currency
from app.api.schemas.currency import *

load_dotenv()

currency_router = APIRouter(prefix="/currency", tags=['currency'])


@currency_router.get("/exchange")
async def exchange_rates_by_code(currency: Annotated[CurrencyScheme, Query()], user: str = Depends(get_current_user)):
    if user and currency:
        return await get_currency(**currency.dict())


@currency_router.get("/convert")
async def convert_currencies(data: Annotated[CurrenciesToConvertScheme, Query()], user: str = Depends(get_current_user)):
    if user and data:
        return await get_currency(**data.dict())


@currency_router.get("/list")
async def available_currencies(user: str = Depends(get_current_user)):
    if user:
        return await get_currency()
