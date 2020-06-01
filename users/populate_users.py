import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'users.settings')


import django

django.setup()

import random
from apptwo.models import User
from faker import Faker

fakegen = Faker()


def populate(N=5):
    for entry in range(0, N):
        Fake_Name = fakegen.name().split()
        Fake_FirstName = Fake_Name[0]
        Fake_LastName = Fake_Name[1]
        Fake_Email = fakegen.email()

        # New Entry
        user = User.objects.get_or_create(FirstName=Fake_FirstName, LastName=Fake_LastName, Email=Fake_Email)[0]
        user.save()

if __name__ == '__main__':
    print("POPULATE")
    populate(20)
    print("Completed")
