from pydantic import BaseModel, Field, PositiveFloat


class CurrenciesToConvertScheme(BaseModel):
    currency_from: str = Field(..., min_length=3, max_length=3)
    currency_to: str = Field(..., min_length=3, max_length=3)
    amount: PositiveFloat

class CurrencyScheme(BaseModel):
    currency: str = Field(..., min_length=3, max_length=3)
