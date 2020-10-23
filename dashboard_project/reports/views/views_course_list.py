import datetime
import csv
from poetfolio.tools import *
from ed.models import *
from ed.forms import *
from ed.tools import *
from vita.models import Student
from django.db.models import Sum
from django.urls import reverse
from django.views import generic
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

# pdf stuff
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle, Spacer, PageBreak
from reportlab.lib import colors
import re

from django.utils.html import strip_tags

@login_required
def CourseListCSV(request, username=None):
    if username is None:
        user = request.user
    elif request.user.username == username:
        user = request.user
    else:
        if is_council(request.user) or is_WSPstaff(request.user):
            user = User.objects.get(username=username)
        else:
            return redirect(reverse('Index'))
    
    allc = all_courses(user)
    response = HttpResponse(content_type='text/csv')
    disposition = f'attachment; filename="{user.username}_courselist.csv"'
    response['Content-Disposition'] = disposition
    
    writer = csv.writer(response)
    writer.writerow(['CRN', 'SUBJ', 'NUM', 'TITLE', 'INSTR',
                     'CR', 'TERM', 'maj1', 'maj2', 'min1', 'min2'
                    ]
                   )
    rows = []
    for c in allc:
        rows.append([c.crn,
                     c.course.subject.short,
                     c.course.number,
                     c.course.title,
                     c.instructor,
                     c.credits,
                     c.term.code,
                     c.maj1,
                     c.maj2,
                     c.min1,
                     c.min2,
                    ]
                   )
    writer.writerows(rows)
    return response

# course list
@login_required
def CourseListPDF(request, username=None):
    if username is None:
        user = request.user
    elif is_council(request.user):
        user = User.objects.get(username=username)
    elif request.user.username == username:
        user = request.user
    else:
        if is_council(request.user):
            user = User.objects.get(username=username)
        else:
            return redirect(reverse('Index'))
    
    student = Student.objects.get(user=user)
    pdf_buffer = io.BytesIO()
    
    p = SimpleDocTemplate(pdf_buffer)
    
    sample_style_sheet = getSampleStyleSheet()
    flowables = []
    
    # title
    title = f'{user.last_name}, {user.first_name} ({student.student_id})'
    flowables.append(Paragraph(title, sample_style_sheet['Title']))
    flowables.append(Spacer(0,5))
    
    # narative
    flowables.append(Paragraph('Narrative', sample_style_sheet['Heading1']))
    flowables.append(Paragraph(f'{strip_tags(student.narrative)}', sample_style_sheet['BodyText']))
    flowables.append(PageBreak())
    
    # goal
    flowables.append(Paragraph('Educational Goals', sample_style_sheet['Heading1']))
    
    edgoals = EducationalGoal.objects.filter(student=user)
    for goal in edgoals:
        flowables.append(Paragraph(f'{goal.title}', sample_style_sheet['Heading2']))
        flowables.append(Paragraph(f'{goal.description}', sample_style_sheet['BodyText']))
        flowables.append(Spacer(0,5))
        
        for course in goal.courses.all():
            flowables.append(Paragraph(f'{course.course.subject.short} {course.course.number}: {course.course.title}', sample_style_sheet['BodyText']))    
       
    flowables.append(PageBreak())

    # major courses
    maj1c = major_courses(user, 1)
    maj2c = major_courses(user, 2)
    
    if maj1c:
        maj1 = Major.objects.get(student=user, number=1)
        flowables.append(Paragraph(f'{maj1.title} (Major)',
                                   sample_style_sheet['Heading1']
                                  )
                        )
        flowables.append(Paragraph(f'{maj1.description}',
                                   sample_style_sheet['BodyText']
                                  )
                        )
        flowables.append(Spacer(0,5))
        data = [ [c.crn,
                  c.course.subject.short,
                  c.course.number,
                  c.course.title,
                  c.credits,
                  c.term,
                 ] for c in maj1c]
        data.insert(0,['CRN', 'SUBJ', 'NUM', 'TITLE', 'CR', 'TERM',])
        LIST_STYLE = TableStyle([('LINEABOVE', (0,0), (-1,0), 2, colors.purple),
                                 ('LINEABOVE', (0,1), (-1,-1), 0.25, colors.black),
                                 ('LINEBELOW', (0,-1), (-1,-1), 2, colors.purple),
                                 ('ALIGN', (1,1), (-1,-1), 'LEFT')
                                ]
                               )
        mytable = Table(data)
        mytable.setStyle(LIST_STYLE)
        flowables.append(mytable)
        flowables.append(Paragraph(f'{maj1c.total} Credits', sample_style_sheet['BodyText']))
    if maj2c:
        maj2 = Major.objects.get(student=user, number=2)
        flowables.append(Paragraph(f'{maj2.title} (Major)',
                                   sample_style_sheet['Heading1']
                                  )
                        )
        flowables.append(Paragraph(f'{maj2.description}',
                                   sample_style_sheet['BodyText']
                                  )
                        )
        flowables.append(Spacer(0,5))
        data = [ [c.crn,
                  c.course.subject.short,
                  c.course.number,
                  c.course.title,
                  c.credits,
                  c.term,
                 ] for c in maj2c]
        data.insert(0,['CRN', 'SUBJ', 'NUM', 'TITLE', 'CR', 'TERM',])
        LIST_STYLE = TableStyle([('LINEABOVE', (0,0), (-1,0), 2, colors.purple),
                                 ('LINEABOVE', (0,1), (-1,-1), 0.25, colors.black),
                                 ('LINEBELOW', (0,-1), (-1,-1), 2, colors.purple),
                                 ('ALIGN', (1,1), (-1,-1), 'LEFT')
                                ]
                               )
        mytable = Table(data)
        mytable.setStyle(LIST_STYLE)
        flowables.append(mytable)
        flowables.append(Paragraph(f'{maj2c.total} Credits', sample_style_sheet['BodyText']))
    #minor courses
    min1c = minor_courses(user, 1)
    min2c = minor_courses(user, 2)

    if min1c:
        min1 = Minor.objects.get(student=user, number=1)
        flowables.append(Paragraph(f'{min1.title} (Minor)',
                                   sample_style_sheet['Heading1']
                                  )
                        )
        flowables.append(Paragraph(f'{min1.description}',
                                   sample_style_sheet['BodyText']
                                  )
                        )
        flowables.append(Spacer(0,5))
        data = [ [c.crn,
                  c.course.subject.short,
                  c.course.number,
                  c.course.title,
                  c.credits,
                  c.term,
                 ] for c in min1c]
        data.insert(0,['CRN', 'SUBJ', 'NUM', 'TITLE', 'CR', 'TERM',])
        LIST_STYLE = TableStyle([('LINEABOVE', (0,0), (-1,0), 2, colors.purple),
                                 ('LINEABOVE', (0,1), (-1,-1), 0.25, colors.black),
                                 ('LINEBELOW', (0,-1), (-1,-1), 2, colors.purple),
                                 ('ALIGN', (1,1), (-1,-1), 'LEFT')
                                ]
                               )
        mytable = Table(data)
        mytable.setStyle(LIST_STYLE)
        flowables.append(mytable)
        flowables.append(Paragraph(f'{min1c.total} Credits', sample_style_sheet['BodyText']))
    if min2c:
        min2 = Minor.objects.get(student=user, number=2)
        flowables.append(Paragraph(f'{min2.title} (Minor)',
                                   sample_style_sheet['Heading1']
                                  )
                        )
        flowables.append(Paragraph(f'{min2.description}',
                                   sample_style_sheet['BodyText']
                                  )
                        )
        flowables.append(Spacer(0,5))
        data = [ [c.crn,
                  c.course.subject.short,
                  c.course.number,
                  c.course.title,
                  c.credits,
                  c.term,
                 ] for c in min2c]
        data.insert(0,['CRN', 'SUBJ', 'NUM', 'TITLE', 'CR', 'TERM',])
        LIST_STYLE = TableStyle([('LINEABOVE', (0,0), (-1,0), 2, colors.purple),
                                 ('LINEABOVE', (0,1), (-1,-1), 0.25, colors.black),
                                 ('LINEBELOW', (0,-1), (-1,-1), 2, colors.purple),
                                 ('ALIGN', (1,1), (-1,-1), 'LEFT')
                                ]
                               )
        mytable = Table(data)
        mytable.setStyle(LIST_STYLE)
        flowables.append(mytable)
        flowables.append(Paragraph(f'{min2c.total} Credits', sample_style_sheet['BodyText']))
 
    # wsp courses  
    flowables.append(Paragraph('WSP', sample_style_sheet['Heading1']))
    WSP = WSPcourses(user)
    data = [ [c.crn,
              c.course.subject.short,
              c.course.number,
              c.course.title,
              c.credits,
              c.term,
             ] for c in WSP]
    data.insert(0,['CRN', 'SUBJ', 'NUM', 'TITLE', 'CR', 'TERM',])
    LIST_STYLE = TableStyle([('LINEABOVE', (0,0), (-1,0), 2, colors.purple),
                             ('LINEABOVE', (0,1), (-1,-1), 0.25, colors.black),
                             ('LINEBELOW', (0,-1), (-1,-1), 2, colors.purple),
                             ('ALIGN', (1,1), (-1,-1), 'LEFT')
                            ]
                           )
    mytable = Table(data)
    mytable.setStyle(LIST_STYLE)
    flowables.append(mytable)
    flowables.append(Paragraph(f'{WSP.total} Credits', sample_style_sheet['BodyText']))
    flowables.append(PageBreak())

    # support courses 
    if supporting_courses(user):
        flowables.append(Paragraph('Supporting Courses', sample_style_sheet['Heading1']))
        supp = supporting_courses(user)
        data = [ [c.crn,
                  c.course.subject.short,
                  c.course.number,
                  c.course.title,
                  c.credits,
                  c.term,
                 ] for c in supp]
        data.insert(0,['CRN', 'SUBJ', 'NUM', 'TITLE', 'CR', 'TERM',])
        LIST_STYLE = TableStyle([('LINEABOVE', (0,0), (-1,0), 2, colors.purple),
                                 ('LINEABOVE', (0,1), (-1,-1), 0.25, colors.black),
                                 ('LINEBELOW', (0,-1), (-1,-1), 2, colors.purple),
                                 ('ALIGN', (1,1), (-1,-1), 'LEFT')
                                ]
                               )
        mytable = Table(data)
        mytable.setStyle(LIST_STYLE)
        flowables.append(mytable)
        flowables.append(Paragraph(f'{supp.total} Credits', sample_style_sheet['BodyText']))
        flowables.append(PageBreak())
    
    # division courses  
    divcourses = courses_by_division(user)
    for key in divcourses:    
        flowables.append(Paragraph(key, sample_style_sheet['Heading1']))
        data = [ [c.crn,
                  c.course.subject.short,
                  c.course.number,
                  c.course.title,
                  c.credits,
                  c.term,
                 ] for c in divcourses[key]]
        data.insert(0,['CRN', 'SUBJ', 'NUM', 'TITLE', 'CR', 'TERM',])
        LIST_STYLE = TableStyle([('LINEABOVE', (0,0), (-1,0), 2, colors.purple),
                                 ('LINEABOVE', (0,1), (-1,-1), 0.25, colors.black),
                                 ('LINEBELOW', (0,-1), (-1,-1), 2, colors.purple),
                                 ('ALIGN', (1,1), (-1,-1), 'LEFT')
                                ]
                               )
        mytable = Table(data)
        mytable.setStyle(LIST_STYLE)
        flowables.append(mytable)
        flowables.append(Paragraph(f'{divcourses[key].total} Credits', sample_style_sheet['BodyText']))
    
    p.build(flowables)
    
    # for this to work, the stream position must be reset to the start
    pdf_buffer.seek(io.SEEK_SET)
    return FileResponse(pdf_buffer,
                        as_attachment=True,
                        filename=f"{user.username}_courselist.pdf"
                       )

    
