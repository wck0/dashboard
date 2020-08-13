# make sure the appropriate venv is activated
# before running this script

# navigate to manage.py in a terminal
# activate the appropriate venv
# ./manage.py shell < path/to/this/script.py

from django.contrib.auth.models import Group
from django.db import IntegrityError

names = (
    'Council',
    'Director',
    'Student',
    'WSP Staff',
)

for name in names:
    try:
        Group.objects.create(name=name)
    except IntegrityError:
        print('Error with', name)

print("Done.")
