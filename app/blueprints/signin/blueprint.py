# This module is the Flask blueprint for the sign-in page (/signin).

from flask import Blueprint, render_template

signin = Blueprint('signin', __name__)


@signin.route('/signin')
def display():
    """
    View function for displaying the sign-in page.

    Parameters:
       None
    Output:
       Rendered HTML page.
    """
    return render_template("admin/signin.html")
