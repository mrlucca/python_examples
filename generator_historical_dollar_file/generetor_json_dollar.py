import os
import json
from datetime import datetime

BASE_DATA_PATH = os.path.join(os.path.abspath("."), "data")
NEW_HISTORICAL_DATA_PATH = os.path.join(BASE_DATA_PATH, "raw_dollar_data.json")
HISTORICAL_DATA_PATH = os.path.join(BASE_DATA_PATH, "dollar_data.json")


def load_data(path: str) -> dict:
    with open(path, "r") as file:
        return json.load(file)


def write_data(data: dict, path: str) -> None:
    with open(path, "w") as file:
        json.dump(data, file, indent=4)


def new_historical_data_exists() -> bool:
    return os.path.exists(NEW_HISTORICAL_DATA_PATH)


def historical_data_exists() -> bool:
    return os.path.exists(HISTORICAL_DATA_PATH)


def transform_raw_data(raw_data: dict) -> dict:
    values = raw_data.get('value')
    if not values:
        raise ValueError("The values are empty")

    struct_dict_data = dict()
    for value in values:
        raw_date = value.get("dataHoraCotacao")
        value = value.get("cotacaoCompra")
        if raw_date and value is not None:
            date = datetime.strptime(raw_date, '%Y-%m-%d %H:%M:%S.%f')
            if not struct_dict_data.get(date.year):
                struct_dict_data[date.year] = {}
            if not struct_dict_data[date.year].get(date.month):
                struct_dict_data[date.year][date.month] = {}

            struct_dict_data[date.year][date.month][date.day] = value

    return struct_dict_data


def append_historical_data(data: dict) -> bool:
    if historical_data_exists():
        cache = load_data(HISTORICAL_DATA_PATH)
    else:
        write_data(data, HISTORICAL_DATA_PATH)
        return historical_data_exists()

    data = json.loads(json.dumps(data))
    for year in data.keys():
        if not cache.get(year):
            cache[year] = {}

        for month in data[year].keys():
            if not cache[year].get(month):
                cache[year][month] = {}

            for day in data[year][month].keys():
                if not cache[year][month].get(day):
                    cache[year][month][day] = data[year][month][day]

    write_data(cache, HISTORICAL_DATA_PATH)
    return historical_data_exists()


def historical_data_generator() -> None:
    if new_historical_data_exists():
        raw_data = load_data(NEW_HISTORICAL_DATA_PATH)
        data = transform_raw_data(raw_data)
        generate = append_historical_data(data)
        if generate:
            print("Generated data!")
        else:
            print("Not generated data!")
    else:
        print("No new data")


if __name__ == "__main__":
    historical_data_generator()
