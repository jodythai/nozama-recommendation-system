# app/models/product_catalog/data_classes.py
"""
Data class for Recommendation Results.
"""

# For more info: https://docs.python.org/3/library/dataclasses.html
from dataclasses import dataclass
from typing import List


@dataclass
class User_Requests:
    """
    Data class for products.
    """
    top_k: str
    predicted_label: str
    prediction_probs: str
    uploaded_filename: str
    prediction_runtime: str
    feature_extraction_runtime: str
    get_neighbors_runtime: str
    request_time: str
    id: str = None

    @staticmethod
    def deserialize(document):
        """
        Helper function for parsing a Firestore document to a Product object.

        Parameters:
            document (DocumentSnapshot): A snapshot of Firestore document.

        Output:
            A Product object.
        """
        data = document.to_dict()
        if data:
            return Product(
                id=document.id,
                top_k=data.get('top_k'),
                predicted_label=data.get('predicted_label'),
                prediction_probs=data.get('prediction_probs'),
                uploaded_filename=data.get('uploaded_filename'),
                prediction_runtime=data.get('prediction_runtime'),
                feature_extraction_runtime=data.get('feature_extraction_runtime'),
                get_neighbors_runtime=data.get('get_neighbors_runtime'),
                request_time=data.get('request_time')
            )

        return None