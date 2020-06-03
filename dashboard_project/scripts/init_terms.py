# make sure the appropriate venv is activated
# before running this script

# navigate to manage.py in a terminal
# activate the appropriate venv
# ./manage.py shell < path/to/this/script.py

from ed.models import Term

years = range(2012, 2025)
ms    = [1, 2, 6, 9]

for y in years:
    for m in ms:
        t = Term(code=100*y+m)
        t.save()

print("Done.")
