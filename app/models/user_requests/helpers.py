# app/models/product_catalog/helpers.py
"""
A collection of helper functions for product related operations.
"""

from dataclasses import asdict
import os
import uuid

from google.cloud import firestore

from .data_classes import User_Requests


BUCKET = os.environ.get('GCS_BUCKET')

firestore_client = firestore.Client()

DOCUMENT_USER_REQUESTS = 'user_requests'

def get_user_requests(user_requests_id):
    result = firestore_client.collection(DOCUMENT_USER_REQUESTS).document(user_requests_id).get()
    return Product.deserialize(result)


def list_user_requests():
    products = firestore_client.collection(DOCUMENT_USER_REQUESTS).order_by('request_time').get()
    product_list = [Product.deserialize(product) for product in list(products)]
    return product_list


def add_user_requests(user_requests):
    user_requests_id = uuid.uuid4().hex
    firestore_client.collection(DOCUMENT_USER_REQUESTS).document(user_requests_id).set(asdict(user_requests))
    return user_requests_id