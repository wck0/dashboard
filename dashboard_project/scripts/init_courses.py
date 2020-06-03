# make sure the appropriate venv is activated
# before running this script

# navigate to manage.py in a terminal
# activate the appropriate venv
# ./manage.py shell < path/to/this/script.py
import json
from ed.models import *

coursejson = 'scripts/courses.json'

with open(coursejson, 'r', encoding="UTF-8") as f:
    course_dict = json.load(f)

for s in course_dict:
    try:
        subj = Subject.objects.get(short=s)
    except:
        continue
    print(subj)
    c = course_dict[s]
    for number in c:
        for y in c[number]:
            for title in y:
                try:
                    Course.objects.get(subject=subj,
                                       number=number,
                                       title=title,
                                      )
                    print("Course {} {} {} already in the database"
                          .format(subj.short, number, title)
                         )
                except:
                    new_course = Course(subject=subj,
                                        number=number,
                                        title=title,
                                       )
                    new_course.save()
                    print("Added {} {} {}".format(subj.short, number, title).encode("UTF-8"))
#    exit()

# plug in 100T, etc., for transfer courses

humanity = Division.objects.get(name="Humanities")
natsci = Division.objects.get(name="Natural Sciences")
socsci = Division.objects.get(name="Social Sciences")

subjs = Subject.objects.filter(department__division=humanity) |        Subject.objects.filter(department__division=natsci) |        Subject.objects.filter(department__division=socsci)

numbs = ('100T', '200T', '300T', '400T')
title = "Transfer"
for subj in subjs:
    for numb in numbs:
        try:
            Course.objects.get(subject=subj, number=numb, title=title)
            print(f"Course {subj.short} {numb} {title} already exists")
        except Course.DoesNotExist:
            new_course = Course(subject=subj, number=numb, title=title)
            new_course.save()
            print(f"Added {subj.short} {numb} {title}")
            
