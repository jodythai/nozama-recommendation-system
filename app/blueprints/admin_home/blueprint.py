# app/blueprints/home/blueprint.py
"""
This module is the Flask blueprint for the product catalog page (/).
"""

from flask import Blueprint, render_template
from middlewares.auth import admin_auth_optional

admin_home = Blueprint('admin_home', __name__)


@admin_home.route('/admin')
@admin_auth_optional
def display(auth_context):
    """
    View function for displaying the admin home page.

    Parameters:
       auth_context (dict): The authentication context of request.
                            See middlewares/auth.py for more information.
    Output:
       Rendered HTML page.
    """

    print(auth_context)
    
    return render_template('admin/home.html',
                           auth_context=auth_context)