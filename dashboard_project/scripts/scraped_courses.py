# make sure the appropriate venv is activated
# before running this script

# navigate to manage.py in a terminal
# activate the appropriate venv
# ./manage.py shell < path/to/this/script.py
#
# expected header is
# CRN
# Crse
# Sect
# Title
# Cr
# GM
# Type
# Days
# Time
# Loc
# Dates
# Instructor
# Fee
# Book
# Max
# Enrl
# AVL
# XL-Max
# XL-Enrl
# Wait
# Rsrvd
# Status
# Lib Ed
# Perm
#
# change coursecsv below as appropriate before running.

import csv
from ed.models import *

terms = ('201609', '201701', '201702', '201709', '201801', '201802',
         '201809', '201901', '201902', '201909', '202001', '202002',
        )

errors = 0
added = 0
exists = 0
for term in terms:
    print('-'*20)
    print(term)
    coursecsv = 'scripts/'+term+'.csv'
    with open(coursecsv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            crse = row['Crse']
            subj, numb = crse.split(' ')
            title = row['Title']
            
            try:
                subject = Subject.objects.get(short=subj)
                Course.objects.get(subject=subject, number=numb, title=title)
                print(f'{subj} {numb} {title} exists')
                exists += 1
            except Subject.DoesNotExist:
                print(f'something wrong with subject {subj}')
                errors += 1
            except Course.DoesNotExist:
                c = Course(subject=subject, number=numb, title=title)
                c.save()
                print(f'{subj} {numb} {title} added')
                added += 1
            except:
                continue
print('done.')
print(added, 'added')
print(exists, 'exist')
print(errors, 'errors')
