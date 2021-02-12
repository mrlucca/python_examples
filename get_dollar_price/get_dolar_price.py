import os 
import json
import sys
from datetime import datetime, timedelta

CACHE_PATH = os.path.join(os.path.abspath("."), "cache")
USD_JSON_PATH = os.path.join(CACHE_PATH, "historical_dollar_data.json")
MAX_RECURSIVE_INTERATION = 100

dollar_values: dict = None


class GetDollarError(Exception):
    ...


def get_dollar_data() -> None or Exception:
    global dollar_values

    if not os.path.exists(USD_JSON_PATH):
        raise GetDollarError("Dollar folder not exixts!")

    with open(USD_JSON_PATH, 'r') as json_file:
        dollar_values = json.load(json_file)


def value_exists(
    day: str, month: str, year: str,
) -> bool:
    if not dollar_values.get(year):
        return False
    if not dollar_values[year].get(month):
        return False
    if not dollar_values[year][month].get(day):
        return False
    return True


def get_recursive_dollar_price(
    date: datetime, recursive: bool = True
) -> float or Exception:
    exists = False
    count = 0
    while not exists and count < MAX_RECURSIVE_INTERATION:
        day, month, year = str(date.day), str(date.month), str(date.year)
        print(f"Try {count} of get dollar value", end=" |> ")
        print(f"get price in: [ {day}/{month}/{year} ]")
        exists = value_exists(day=day,month=month,year=year)
        if not recursive: break
        date = date - timedelta(days=1)
        count += 1

    if exists:
        return dollar_values[year][month][day]
    else:
        raise GetDollarError("Dollar value not exists")


if __name__ == "__main__":
    get_dollar_data()
    for argv in sys.argv:
        if "@day" in argv:
            """ ex: @day='DD/MM/YYYY' """
            _, date = argv.split("=")
            date = datetime.strptime(date, "%d/%m/%Y")
            value = get_recursive_dollar_price(date)
            print(f"Dolar value {value}")

        if "@test" in argv:
            date = datetime.now() + timedelta(days=5)
            value = get_recursive_dollar_price(date)
            print(f"Dolar value {value}")
