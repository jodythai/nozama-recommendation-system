import re
import os
import base64
import time
import sys
import numpy as np
import uuid
import json
import tensorflow as tf
import requests
from tensorflow.keras.models import Model
from flask import Blueprint, request, jsonify, current_app, render_template
from google.cloud import storage
from annoy import AnnoyIndex
from models import product_catalog, user_requests

recommend = Blueprint('recommend', __name__)

CLOUD_FUNC_RECOMMEND_URL = ''

@recommend.route('/recommend', methods=['GET', 'POST'])
def handle_recommend():  

    if request.method == 'POST':
        
        data = request.get_json()

        response = requests.post(CLOUD_FUNC_RECOMMEND_URL, json = data)
        
        response_dict = json.loads(response.text)
        top_k = response_dict['top_k']

        # get product details
        products = []
        for item in top_k:
            product_id = item['asin']
            products.append(product_catalog.get_product(product_id))

        # Log user_request to firestore database
        user_requests_obj = user_requests.User_Requests(top_k=str(top_k),
                                                        predicted_label=response_dict['predicted_label'],
                                                        prediction_probs=str(response_dict['prediction_probs']),
                                                        uploaded_filename=response_dict['uploaded_filename'],
                                                        prediction_runtime=response_dict['prediction_runtime'],
                                                        feature_extraction_runtime=response_dict['feature_extraction_runtime'],
                                                        get_neighbors_runtime=response_dict['get_neighbors_runtime'],
                                                        request_time=response_dict['request_time'])

        user_requests_id = user_requests.add_user_requests(user_requests_obj)

        products_html = render_template('list_products_from_recommend.html', products = products)

    return (jsonify({'products_html': products_html}))