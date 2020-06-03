# make sure the appropriate venv is activated
# before running this script

# navigate to manage.py in a terminal
# activate the appropriate venv
# ./manage.py shell < path/to/this/script.py

from ed.models import Division, Department

divs = {}

for i in range(1,6):
    divs[i] = Division.objects.filter(code=i).get()

depts = [
         ("Art & Art History", 1),
         ("English Language & Literature", 1),
         ("History", 1),
         ("Modern Languages & Literatures", 1),
         ("Music", 1),
         ("Philosophy", 1),
         ("Religious Studies", 1),
         ("Theatre Arts & Communication", 1),
         ("Biology", 2),
         ("Chemistry", 2),
         ("Environmental Science", 2),
         ("Mathematics & Computer Science", 2),
         ("Physics & Astronomy", 2),
         ("Business Administration", 3),
         ("Economics", 3),
         ("Education & Child Development", 3),
         ("Kinesiology", 3),
         ("Political Science", 3),
         ("Psychological Sciences", 3),
         ("Sociology & Anthropology", 3),
         ("Social Work", 3),
         ("Gender Studies", 4),
         ("Global & Cultural Studies", 4),
         ("Interdisciplinary", 4),
         ("Organizational Leadership", 4),
         ("Whittier Scholars Program", 4),
         ("Athletics", 5),
         ("Healthcare Leadership Program", 4),
        ]

for n, d in depts:
    dept = Department(name=n, division=divs[d])
    if not Department.objects.filter(name=n):
        try:
            dept.save()
            print("Added {} to the database".format(n))
        except:
            print("Something went wrong with {}".format(n))
    else:
        print("It looks like {} is already in the database.".format(n))

print("Done.")
