#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from store.models import Product

def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

def prepopulate_products():
    Product.objects.create(name='Produto 1', price=19.99, digital=0, image='headphones.jpg')
    Product.objects.create(name='Produto 2', price=12.99, digital=0, image='headphones1.jpg')
    # Adicione mais produtos conforme necessário


if __name__ == "__main__":
    main()
    prepopulate_products()
