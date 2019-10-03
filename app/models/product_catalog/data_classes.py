# app/models/product_catalog/data_classes.py
"""
Data class for products.
"""

# For more info: https://docs.python.org/3/library/dataclasses.html
from dataclasses import dataclass
from typing import List


@dataclass
class Product:
    """
    Data class for products.
    """
    title: str
    category: str
    brand: str
    imUrl: str
    price: float
    rating: float
    created_at: int
    asin: str
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
                asin=data.get('asin'),
                title=data.get('title'),
                category=data.get('category'),
                brand=data.get('brand'),
                imUrl=data.get('imUrl'),
                price=data.get('price'),
                rating=data.get('rating'),
                created_at=data.get('created_at')
            )

        return None