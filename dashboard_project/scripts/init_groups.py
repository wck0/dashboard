# make sure the appropriate venv is activated
# before running this script

# navigate to manage.py in a terminal
# activate the appropriate venv
# ./manage.py shell < path/to/this/script.py

from django.contrib.auth.models import Group

names = ('Council', 
         'Director',
         'Student',
         'WSP Staff',
        )
for name in names:
    try:
        Group.objects.create(name=name)
    except:
        print('Error with', name)

print("Done.")
