"""
This module includes decorators for authenticating requests.
"""

from functools import wraps
from flask import redirect, request, url_for

from firebase_admin import auth


def verify_firebase_id_token(token):
    """
    A helper function for verifying ID tokens issued by Firebase.
    See https://firebase.google.com/docs/auth/admin/verify-id-tokens for
    more information.

    Parameters:
       token (str): A token issued by Firebase.

    Output:
       auth_context (dict): Authentication context.
    """
    try:
        full_auth_context = auth.verify_id_token(token)
    except ValueError:
        return {}

    auth_context = {
        'username': full_auth_context.get('name'),
        'uid': full_auth_context.get('uid'),
        'email': full_auth_context.get('email')
    }
    return auth_context


def admin_auth_required(f):
    """
    A decorator for view functions that require authentication.
    If signed in, pass the request to the decorated view function with
    authentication context; otherwise redirect the request.

    Parameters:
       f (func): The view function to decorate.

    Output:
       decorated (func): The decorated function.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        firebase_id_token = request.cookies.get('firebase_id_token')
        if not firebase_id_token:
            return redirect(url_for('admin_login.display'))

        auth_context = verify_firebase_id_token(firebase_id_token)
        if not auth_context:
            return redirect(url_for('admin_login.display'))

        return f(auth_context=auth_context, *args, **kwargs)
    return decorated

def admin_auth_optional(f):
    """
    A decorator for view functions where authentication is optional.
    If signed in, pass the request to the decorated view function with
    authentication context.

    Parameters:
       f (func): The view function to decorate.

    Output:
       decorated (func): The decorated function.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        firebase_id_token = request.cookies.get('firebase_id_token')
        if not firebase_id_token:
            return f(auth_context=None, *args, **kwargs)

        auth_context = verify_firebase_id_token(firebase_id_token)
        if not auth_context:
            return f(auth_context=None, *args, **kwargs)

        return f(auth_context=auth_context, *args, **kwargs)
    return decorated