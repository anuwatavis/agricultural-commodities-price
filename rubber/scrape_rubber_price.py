import json
import os
from numpy import result_type
import pandas as pd
from selenium import webdriver
import datetime
import requests
import pandas as pd

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver', chrome_options=chrome_options)
json_directory = "../dataset"

logs = ''
today = datetime.datetime.now()


def extract_data_from_table():
    # select lastes update row
    row_selected = driver.find_elements_by_xpath(
        '//*[@id="ewt_main_structure"]/tbody/tr[3]/td/div/center/table/tbody/tr/td[2]/table[2]/tbody/tr[3]')
    row = row_selected[0]
    data = row.find_elements_by_tag_name("td")
    date = data[0].text
    raw_robber_price = data[2].text
    latex_price = data[5].text
    raw_robber_sheet_price = data[8].text
    raw_robber_sheet_level_3_price = data[11].text
    rss_3_price = data[17].text
    market = data[20].text
    fob_rss3_price = data[23].text
    return {"date": date,
            "raw_robber_price": raw_robber_price,
            "latex_price": latex_price,
            "raw_robber_sheet_price": raw_robber_sheet_price,
            "raw_robber_sheet_level_3_price": raw_robber_sheet_level_3_price,
            "rss_3_price": rss_3_price,
            "market": market,
            "fob_rss3_price": fob_rss3_price}


def thai_month_mapping(thai_month_input):
    # create thai month dict for mapping thai month from website
    thai_month = {
        "มกราคม": 1,
        "กุมภาพันธ์": 2,
        "มีนาคม": 3,
        "เมษายน": 4,
        "พฤษภาคม": 5,
        "มิถุนายน": 6,
        "กรกฎาคม": 7,
        "สิงหาคม": 8,
        "กันยายน": 9,
        "ตุลาคม": 10,
        "พฤศจิกายน": 11,
        "ธันวาคม": 12,
    }
    # check input correct
    if thai_month_input in thai_month:
        return (True, thai_month[thai_month_input])
    else:
        return (False, "Invalid Month")


def extract_date_from_thai_date(raw_date_in_web):
    try:
        result = raw_date_in_web.split(" ")
        date = int(result[0])
        (mapping_success, month) = thai_month_mapping(result[1])
        year = int(result[2]) - 543
        if(mapping_success):
            date_object = datetime.datetime(year, month, date)
            return (True, date_object)
        else:
            return (False, 'Invalid Thai Month Input')
    except Exception as e:
        return (False, 'Invalid Thai Date Input')


def scrape_rubber_price():
    scrape_result = extract_data_from_table()
    return scrape_result


def dump_json_to_dateset(data_dict):
    os.makedirs(json_directory, exist_ok=True)
    result_data = {
        "data": data_dict,
    }
    with open(f'{json_directory}/rubber_price.json', 'w', encoding='utf8') as json_file:
        json.dump(result_data, json_file, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    # Define url for scrape
    URL = 'https://www.raot.co.th/rubber2012/menu5.php'
    driver.get(URL)
    scrape_result = scrape_rubber_price()
    (extract_date_success, extracted_date) = extract_date_from_thai_date(
        scrape_result['date'])
    if(extract_date_success):
        scrape_result['date'] = str(extracted_date)
        dump_json_to_dateset(scrape_result)
    driver.quit()
