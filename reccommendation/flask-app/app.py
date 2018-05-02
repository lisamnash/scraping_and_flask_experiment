from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
import json

from helper_functions import convert_product_number
from helper_functions import get_img_filename
from helper_functions import get_result_list
from helper_functions import get_phone_names
from helper_functions import convert_to_product_number
from helper_functions import get_phone_data

app = Flask(__name__)


@app.route('/')
def homepage():
    phone_names = list(get_phone_names())

    return render_template('landing_page.html', phones=phone_names)


@app.route('/display/')
def show_similar(data=None):
    product_number = request.args.get('product')

    if request.args.get('results'):
        top_results = request.args.get('results')
    else:
        top_results = 5

    data = get_result_list(product_number, number=top_results)
    # now let's get the images
    return_data = []
    for number in data['recs']:
        phone_img_filename = get_img_filename(number)
        image_url = url_for('static', filename='full/' + phone_img_filename)
        return_dict = {'image_url': image_url,
                       'name': convert_product_number(number)
                       }
        return_data.append(return_dict)
        data['metadata_and_images'] = return_data

    return render_template('similar_phones.html', data=data)


@app.route('/test_bootstrap/')
def display():
    product_number = request.args.get('product')
    phone_names = list(get_phone_names())

    if not product_number:
        product_number = '258657'
    else:
        try:
            product_number = int(product_number)
        except ValueError:
            # let's convert this to a product number

            product_number = convert_to_product_number(product_number)

    single_phone_data = get_phone_data(product_number)
    print(single_phone_data)
    if request.args.get('results'):
        top_results = request.args.get('results')
    else:
        top_results = 3

    data = get_result_list(product_number, number=top_results)
    phone_img_filename = get_img_filename(product_number)
    image_url = url_for('static', filename='full/' + phone_img_filename)
    data['product_image_url'] = image_url
    # now let's get the images
    return_data = []
    for number in data['recs']:
        phone_img_filename = get_img_filename(number)
        image_url = url_for('static', filename='full/' + phone_img_filename)
        return_dict = {'image_url': image_url,
                       'name': convert_product_number(number)
                       }
        return_data.append(return_dict)
        data['metadata_and_images'] = return_data
    return render_template('bootstrap_album.html', data=data, phones=phone_names, single_data = single_phone_data)

