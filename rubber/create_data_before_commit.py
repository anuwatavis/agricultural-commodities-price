import datetime
import json
import os

import pandas as pd
import requests

json_directory = "../dataset"
logs = ''
today = datetime.datetime.now()


def get_current_year_rubber_prices():
    response = requests.get(
        f'https://raw.githubusercontent.com/wiki/anuwatavis/agricultural-commodities-price/rubber_data/rubber_price_{today.year}.json')
    data_json = response.json()
    return data_json


if __name__ == '__main__':

    # load lastest update from wiki
    current_year_record = get_current_year_rubber_prices()
    lastest_update_df = pd.json_normalize(current_year_record['data'])

    # load new record from artifact download
    new_record = pd.read_json('../wiki/rubber_data/rubber_price.json').T
    new_record['date'] = pd.to_datetime(new_record['date'])
    new_record.reset_index(drop=True, inplace=True)

    # merge
    frames = [lastest_update_df, new_record]
    result_df = pd.concat(frames)
    result_df['date'] = pd.to_datetime(result_df['date'])
    result_df.drop_duplicates(subset=['date'], keep='last', inplace=True)
    result_df.reset_index(drop=True, inplace=True)
    result = result_df.to_json(orient='records', indent=2, date_format='iso')

    update_data = json.loads(result)

    result_json = {
        "update_date": str(today),
        "data": update_data,
        "data_dictionary": {
            "date": "วันที่",
            "raw_robber_price": "ยางแผ่นดิบ",
            "latex_price": "น้ำยางสด(ณ โรงงาน)",
            "raw_robber_sheet_price": "ยางแผ่นดิบ",
            "raw_robber_sheet_level_3_price": "ยางแผ่นรมควัน ชั้น3",
            "rss_3_price": "Rss3 สูงสุด",
            "market": "ตลาดกลาง",
            "fob_rss3_price": "FOB. RSS3(Bangkok)"
        },
        "source_reference": ["การยางแห่งประเทศไทย"]
    }
    os.makedirs(json_directory, exist_ok=True)
    with open(f'{json_directory}/rubber_price_{today.year}.json', 'w', encoding='utf8') as json_file:
        json.dump(result_json, json_file, ensure_ascii=False, indent=2)
