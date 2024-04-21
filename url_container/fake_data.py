import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE',  'url_container.settings')
django.setup()

import random
from catalog.models import Collection, Container
from user.models import CustomUser
from faker import Faker



fake = Faker()


for _ in range(0):
    user_data = {
        'email': fake.email(),
        'password': fake.password()
    }

    CustomUser.objects.create(**user_data)


random_user = random.choice(CustomUser.objects.all())
container = Container.objects.create(user=random_user)

for _ in range(0):
    collections_data ={
        'name': fake.word(),
        'description': fake.text(),
        'user': random_user
    }

    Collection.objects.create(**collections_data)


url_types = ['website', 'article', 'video', 'book', 'music']


for _ in range(200):
    container_data ={
        'title': fake.word(),
        'description': fake.text(),
        'url': fake.url(),
        'url_type': random.choice(url_types),
        'user': random.choice(CustomUser.objects.all())
    }

    Container.objects.create(**container_data)



