import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")

import django
import random
from faker import Faker

import numpy as np

django.setup()
from products.models import Category, Product

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")



fake = Faker()

id_category = fake.random_int(max=10)

def category(value):
    for i in range(10):
        name = fake.name()
        description = fake.text()
        new_category = Category.objects.get_or_create(name=name, description=description)

def product(value):
    for i in range(value):
        name = fake.name()
        description = fake.text()
        new_product = Product.objects.get_or_create(category_id_id=id_category, name=name, description=description, price=fake.random_int(max=1000))

def main():
    no = int(input("Количество: "))
    category(no)
    product(no)

if __name__ == '__main__':
    main()




