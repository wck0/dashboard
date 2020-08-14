# make sure the appropriate venv is activated
# before running this script

# navigate to manage.py in a terminal
# activate the appropriate venv
# ./manage.py shell < path/to/this/script.py

from ed.models import Division
from django.db.utils import IntegrityError

divs = {
        1: "Humanities",
        2: "Natural Sciences",
        3: "Social Sciences",
        4: "Interdisciplinary",
        5: "Non-Academic",
       }

for code, name in divs.items():
    d = Division(code=code, name=name)
    try:
        d.save()
        print("Added {} {} to the database".format(code, name))
    except IntegrityError as e:
        print("Could not add (probably duplicate code)")
print("Done.")
