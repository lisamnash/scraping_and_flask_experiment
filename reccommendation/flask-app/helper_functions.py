import json

import pandas as pd

PHONE_DATA_FILE = '/Users/lisa/client_projects/major-tom/reccommendation/data/csl.csv'
RECOMMENDATION_DATA_FILE = '/Users/lisa/client_projects/major-tom/reccommendation/data/similar.json'

# with open(PHONE_DATA_FILE) as json_data:
#     PHONE_DATA = json.load(json_data)

PHONE_DATA = pd.read_csv(PHONE_DATA_FILE)

with open(RECOMMENDATION_DATA_FILE) as json_data:
    RECOMMENDATION_DATA = json.load(json_data)


def get_result_list(product_number, number=5):
    recs = RECOMMENDATION_DATA[product_number][:number]
    product = PHONE_DATA[PHONE_DATA.product_name == float(product_number)].Product_Number.values[0]
    return {'product': product, 'recs': recs}


def get_img_filename(product_number):
    return PHONE_DATA[PHONE_DATA.product_name == float(product_number)].image.values[0]


def convert_product_number(product_number):
    return PHONE_DATA[PHONE_DATA.product_name == float(product_number)].Product_Number.values[0]


def get_phone_names():
    phone_names = PHONE_DATA.Product_Number.values
    return phone_names


def convert_to_product_number(product_name):
    product_name = product_name.strip()
    return str(PHONE_DATA[PHONE_DATA.Product_Number == product_name].product_name.values[0])


def get_phone_data(product_number):
    single_phone_data = PHONE_DATA[PHONE_DATA.product_name == float(product_number)][
        ['Main Camera Resolution', 'RAM', 'Internal Memory', 'Weight (g)', 'Display Size (inch)', 'Battery Capacity']]

    data = []
    for col in single_phone_data.columns.values:
        data.append([col, single_phone_data[col].values[0]])

    return data
