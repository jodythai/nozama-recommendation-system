from functools import wraps

from flask_wtf import FlaskForm
from wtforms import FieldList, FloatField, StringField
from wtforms.validators import DataRequired, Optional


class UploadForm(FlaskForm):
    """
    FlaskForm for selling items.
    """
    image = StringField('image', validators=[DataRequired()])

def upload_form_validation_required(f):
    """
    A decorator for validating requests with the upload form.
    Returns an error message if validation fails.

    Parameters:
       f (func): The view function to decorate.

    Output:
       decorated (func): The decorated function.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        upload_form = UploadForm()
        if not upload_form.validate():
            return 'Something does not look right. Check your input and try again.', 400

        return f(form=upload_form, *args, **kwargs)
    return decorated