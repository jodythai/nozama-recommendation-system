# app/models/product_catalog/helpers.py
"""
A collection of helper functions for product related operations.
"""

from dataclasses import asdict
import os
import uuid

from google.cloud import firestore

from .data_classes import Product


BUCKET = os.environ.get('GCS_BUCKET')

firestore_client = firestore.Client()

DOCUMENT_PRODUCTS = 'products_amazon'

def get_product(product_id):
    """
    Helper function for getting a product.

    Parameters:
        product_id (str): The ID of the product.

    Output:
        A Product object.
    """
    products = firestore_client.collection(DOCUMENT_PRODUCTS).where('asin', '==', product_id).get()
    for item in products:
        product = item
    return Product.deserialize(product)


def list_products():
    """
    Helper function for listing products.

    Parameters:
        None.

    Output:
        A list of Product objects.
    """

    products = firestore_client.collection(DOCUMENT_PRODUCTS).order_by('created_at').get()
    product_list = [Product.deserialize(product) for product in list(products)]
    return product_list