# make sure the appropriate venv is activated
# before running this script

# navigate to manage.py in a terminal
# activate the appropriate venv
# ./manage.py shell < path/to/this/script.py

from vita.models import Student
from vita.models import OffCampusExperience
from django.db.utils import IntegrityError

students = Student.objects.all()

for student in students:
    try:
        oce = OffCampusExperience.objects.get(student=student)
        print(f"OCE exists for {student}")
    except OffCampusExperience.DoesNotExist:
        oce = OffCampusExperience.objects.create(student=student)
        oce.save()
        print(f"Created OCE for {student}")
