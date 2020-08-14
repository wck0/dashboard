# make sure the appropriate venv is activated
# before running this script

# navigate to manage.py in a terminal
# activate the appropriate venv
# ./manage.py shell < path/to/this/script.py

from django.db import IntegrityError
from ed.models import Subject, Department

subjs = [
    ("Anthropology", "ANTH", "Sociology & Anthropology"),
    ("Athletics", "APA", "Athletics"),
    ("Art", "ART", "Art & Art History"),
    ("Biology", "BIOL", "Biology"),
    ("Business Administration", "BSAD", "Business Administration"),
    ("Child Development", "CHDV", "Education & Child Development"),
    ("Chemistry", "CHEM", "Chemistry"),
    ("Computer Science", "COSC", "Mathematics & Computer Science"),
    ("Economics", "ECON", "Economics"),
    ("Education", "EDUC", "Education & Child Development"),
    ("English", "ENGL", "English Language & Literature"),
    ("Environmental Studies", "ENST", "Environmental Science"),
    ("Environmental Science", "ENVS", "Environmental Science"),
    ("Film", "FILM", "Theatre Arts & Communication"),
    ("French", "FREN", "Modern Languages & Literatures"),
    ("Global & Cultural Studies", "GCS", "Global & Cultural Studies"),
    ("History", "HIST", "History"),
    ("Interdisciplinary", "INTD", "Interdisciplinary"),
    ("Japanese", "JAPN", "Modern Languages & Literatures"),
    ("Kinesiology", "KNS", "Kinesiology"),
    ("Mathematics", "MATH", "Mathematics & Computer Science"),
    ("Music", "MUS", "Music"),
    ("Organizational Leadership", "ORGL", "Organizational Leadership"),
    ("Philosophy", "PHIL", "Philosophy"),
    ("Physics", "PHYS", "Physics & Astronomy"),
    ("Political Science", "PLSC", "Political Science"),
    ("Psychology", "PSYC", "Psychological Sciences"),
    ("Religious Studies", "REL", "Religious Studies"),
    ("Sociology", "SOC", "Sociology & Anthropology"),
    ("Social Work", "SOWK", "Social Work"),
    ("Spanish", "SPAN", "Modern Languages & Literatures"),
    ("Theatre", "THEA", "Theatre Arts & Communication"),
    ("Healthcare Leadership", "WCHL", "Healthcare Leadership Program"),
    ("Whittier Scholars", "WSP", "Whittier Scholars Program"),
]

for n, s, d in subjs:
    try:
        dept = Department.objects.get(name=d)
    except Department.DoesNotExist:
        print("Problem with {} in department {}".format(s, d))
        continue
    subj = Subject(name=n, short=s, department=dept)
    if not Subject.objects.filter(name=n).count():
        try:
            subj.save()
            print("Added {} to the database".format(s))
        except IntegrityError:
            print("Something went wrong with {}".format(s))
    else:
        print("{} is already in the database".format(s))

print("Done.")
