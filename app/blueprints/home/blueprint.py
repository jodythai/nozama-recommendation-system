# app/blueprints/home/blueprint.py
"""
This module is the Flask blueprint for the product catalog page (/).
"""

from flask import Blueprint, render_template, request, jsonify
from models import product_catalog

home_page = Blueprint('home_page', __name__)


@home_page.route('/', methods=['GET'])
def display():
    """
    View function for displaying the home page.

    Output:
       Rendered HTML page.
    """

    # products = product_catalog.list_products()

    return render_template('home.html')
