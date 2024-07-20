from pydantic import BaseModel, constr
from datetime import datetime


class CurrencyConversion(BaseModel):
    input_currency: constr(min_length=3, max_length=3)
    output_currency: constr(min_length=3, max_length=3) = None
    amount: float = None
    date: str = None
    operation_type: str


class CurrencyRate(BaseModel):
    input_currency: constr(min_length=3, max_length=3)
    output_currency: constr(min_length=3, max_length=3)
    date: str = datetime.today().strftime("%d.%m.%y")
    rate: float
    operation_type: str


class User(BaseModel):
    username: str
    password: str
