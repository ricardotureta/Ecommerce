import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings")
django.setup()

from django.contrib.auth.models import User

def create_super_user():
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@hotmail.com', 'admin')

from store.models import Product

def create_products():
    Product.objects.create(name='Fones de ouvido', price=199.99, digital=0, image='headphones.jpg')
    Product.objects.create(name='Carregador', price=20.99, digital=0, image='shirt.jpg')
    Product.objects.create(name='Cabo HDMI', price=199.99, digital=0, image='shoes.jpg')
    Product.objects.create(name='Notebook', price=2999.99, digital=0, image='sourcecode.jpg')
    Product.objects.create(name='TV Smart curva', price=1999.99, digital=0, image='tv.jpg')
    Product.objects.create(name='Celular', price=999.99, digital=0, image='watch.jpg')


if __name__ == '__main__':
    create_super_user()
    create_products()
