from datetime import datetime
from typing import List

from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from models import User, CurrencyConversion, CurrencyRate
import uvicorn

import txt_editor

txt_editor = txt_editor.txtEditor()
app = FastAPI()

security = HTTPBasic()
USER_DATA = [User(**{"username": "admin", "password": "admin"})]


def select_last_date(pairs):
    latest_pairs = {}

    for pair in pairs:
        value_out = pair['value_out'][0]

        if value_out not in latest_pairs:
            latest_pairs[value_out] = pair
        else:
            date_str = pair['date'][0]
            date = datetime.strptime(date_str, '%d.%m.%y')

            existing_date_str = latest_pairs[value_out]['date'][0]
            existing_date = datetime.strptime(existing_date_str, '%d.%m.%y')

            if date > existing_date:
                latest_pairs[value_out] = pair

    return list(latest_pairs.values())


def select_pairs(currency_conversion: CurrencyConversion, pairs: list):
    pairs = [pair for pair in pairs
             if pair["value_in"][0] == currency_conversion.input_currency
             and pair["type"][0] == currency_conversion.operation_type
             and (currency_conversion.date is None or pair["date"][0] == currency_conversion.date)
             and (currency_conversion.output_currency is None
                  or pair["value_out"][0] == currency_conversion.output_currency)]
    return select_last_date(pairs)


def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user_from_db(credentials.username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    elif user.password != credentials.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password")

    return True


def get_user_from_db(login: str):
    for user in USER_DATA:
        if user.username == login:
            return user
    return None


@app.post("/convert_currency")
async def convert_currency(currency_conversion: CurrencyConversion):  # Реализация конвертации валюты
    if not currency_conversion.output_currency:
        raise Exception("Нет выходной валюты")
    if currency_conversion.amount is None:
        raise Exception("Нет суммы для перевода")

    pairs = select_pairs(currency_conversion, txt_editor.read_pairs())[0]
    rate = pairs["rate"][0]
    amount = currency_conversion.amount * float(rate)

    return {"amount": amount, "output_currency": currency_conversion.output_currency}


@app.post("/get_rate")
async def get_rate(currency_conversion: CurrencyConversion):  # Реализация получения курса валюты
    pairs = txt_editor.read_pairs()
    pairs = select_pairs(currency_conversion, pairs)
    return pairs


@app.post("/add_currency")
async def add_currency(currency_rates: List[CurrencyRate], user: User = Depends(authenticate_user)):
    for currency_rate in currency_rates:
        txt_editor.add_pairs(currency_rate.dict())
    return {"message": "New rate succesfully added."}


if __name__ == '__main__':
    uvicorn.run(app,
                host='127.0.0.1',
                port=8080)
