import datetime
from poetfolio.tools import *
from ed.models import *
from ed.forms import *
from ed.tools import *
from vita.models import Student
from siteconfig.models import HeroImage
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

import logging
logger = logging.getLogger(__name__)

try:
    hero = HeroImage.objects.get(app='ed')
#except HeroImage.DoesNotExist:
#    hero = HeroImage.objects.get(app='default')
except:
    hero = None

#Displays all courses that the user has
#Defaults to Index if no other return is hit
#fix login_required error
@login_required
def CourseList(request, username=None): 
    user = request.user

    # POST request handle staff/council
    if request.method == 'POST':

        #looking for staff or council
        if is_WSPstaff(user) or is_council(user):
            try:
                student = User.objects.get(id=request.POST.get('student'))
            except User.DoesNotExist:
                return redirect(reverse('CourseList'))

            return redirect(reverse('CourseList')+student.username)


        else:
            return redirect(reverse('Index'))

    # GET request handle student and staff/council
    elif request.method == 'GET':
        #students
        if is_student(user):
            studentcourses = all_courses(user)
            return render(request, 'ed/courselist.html',
                                  {'pagename': "Course List",
                                   'user': user,
                                   'usercourses': studentcourses,
                                   'hero': hero,
                                  }
                         )
        #staff/council
        elif is_WSPstaff(user) or is_council(user):
            if username is None:
                studentlist = all_students()

                return render(request, 'ed/studentpickerform.html',
                                      {'pagename': "Select Student",
                                       'students': studentlist,
                                       'target': 'CourseList',
                                       'hero': hero,
                                      }
                             )
            else:
                student = User.objects.get(username=username)
                studentcourses = all_courses(student)
                divcourses = courses_by_division(student)
                major1 = major_courses(student, 1)
                major2 = major_courses(student, 2)
                minor1 = minor_courses(student, 1)
                minor2 = minor_courses(student, 2)
                wspcourses = WSPcourses(student)
                support = supporting_courses(student)
                edgoals = EducationalGoal.objects.filter(student=user)

                return render(request, 'ed/all.html',
                             {'pagename': student.get_full_name() + " Course list",
                              'user': student,
                              'usercourses': studentcourses,
                              'divcourses': divcourses,
                              'major1': major1,
                              'major2': major2,
                              'minor1': minor1,
                              'minor2': minor2,
                              'wspcourses': wspcourses,
                              'support': support,
                              'edgoals': edgoals,
                              'hero': hero,
                             })

        else:
            #no groups
            return redirect(reverse('Index'))

    # not GET or POST request
    else:
        return redirect(reverse('Index'))

##Displays all courses that are offered
#@login_required
#def AllCourses(request, subj=''):

#    if subj:
#        subject = Subject.objects.get(short=subj)
#        listofcourses = Course.objects.filter(subject=subject)
#    else:
#        listofcourses = Course.objects.all() #list of course objects
#    context = {
#            'usercourses':listofcourses,
#            'pagename': "All Courses",
#            'hero': hero,
#    }

#    return render(request, 'ed/allcourses.html', context)

@login_required
def EditEDCourse(request, edcourse_id=None):
    user = request.user
    if not is_student(user):
        return redirect(reverse('Index'))

    if request.method == 'GET':
        if edcourse_id:
            try:
                edcourse = EDCourse.objects.get(student=user, id=edcourse_id)
            except EDCourse.DoesNotExist:
                return redirect(reverse('Index'))
            year = datetime.date.today().year
            subjects = Subject.objects.all()
            years = [i for i in range(year-4, year+4)]
            subjs = [s.short for s in subjects]
            return render(request, 'ed/editEDCourse.html',
                               {'pagename':'Edit Course',
                                'subjects':subjs,
                                'years':years,
                                'user':user,
                                'edcourse':edcourse,
                                'hero': hero,
                               }
                     )
        else:
            return render(request, 'ed/editEDCourse.html', {})

    elif (edcourse_id is not None) and (request.method == 'POST'):
        subj = request.POST.get('subject')
        num = request.POST.get('number')
        title = request.POST.get('title')
        term = request.POST.get('term')
        year = request.POST.get('year')
        cr = request.POST.get('credits')
        crn = request.POST.get('crn')
        instructor = request.POST.get('instructor')
        completed = request.POST.get('completed')
        maj1 = request.POST.get('maj1')
        maj2 = request.POST.get('maj2')
        min1 = request.POST.get('min1')
        min2 = request.POST.get('min2')
        is_whittier = request.POST.get('is_whittier')
        notes = request.POST.get('notes')

        term = Term.objects.get(code=(year+term))

        if not cr:
            cr = 0

        if int(completed) > 0:
            completed = True
        else:
            completed = False
        
        if int(maj1) > 0:
            maj1 = True
        else:
            maj1 = False

        if int(maj2) > 0:
            maj2 = True
        else:
            maj2 = False

        if int(min1) > 0:
            min1 = True
        else:
            min1 = False

        if int(min2) > 0:
            min2 = True
        else:
            min2 = False

        if int(is_whittier) > 0:
            is_whittier = True
        else:
            is_whittier = False

        if (subj and num and title and term):
            #look into getobjector404
            course = Course.objects.get(subject__short = subj,
                                        number = num,
                                        title = title,
                                       )
            edcourse = EDCourse.objects.get(id=edcourse_id)
            if edcourse.student == user:
                edcourse.course = course
                edcourse.term = term
                edcourse.credits = cr
                edcourse.completed = completed
                edcourse.instructor = instructor 
                edcourse.maj1 = maj1
                edcourse.maj2 = maj2 
                edcourse.min1 = min1
                edcourse.min2 = min2
                edcourse.is_whittier = is_whittier
                edcourse.notes = notes

                if crn.isdigit():
                    edcourse.crn = crn
                #some checking maybe?
                edcourse.save()
                return redirect(reverse('CourseList'))
            else:
                return redirect(reverse('Index'))
        return redirect(reverse('CourseList'))
    
    return redirect(reverse('Index'))

#Allows user to add an EDCourse object (class) to their ED
@login_required
def AddCourse(request):
    user = request.user
    if request.method == 'GET':

        #student only
        if not is_student(user):
            return redirect(reverse('Index'))

        year = datetime.date.today().year
        subjects = Subject.objects.all()
        years = [i for i in range(year-4, year+4)]
        subjs = [s.short for s in subjects]

        studentcourses = all_courses(user)

        return render(request, 'ed/AddEDCourse.html', 
                              {'subjects':sorted(subjs),
                               'years':years,
                               'user': user,
                               'usercourses':studentcourses,
                               'hero': hero,
                              }
                     )

    elif request.method == 'POST':

        if not is_student(user):
            return redirect(reverse('Index'))
        
        subjs = request.POST.getlist('subject')
        nums = request.POST.getlist('number')
        titles = request.POST.getlist('title')
        terms = request.POST.getlist('term')
        years = request.POST.getlist('year')
        crs = request.POST.getlist('credits')
        crns = request.POST.getlist('crn')
        instructors = request.POST.getlist('instructor')
        completeds = request.POST.getlist('completed')
        maj1s = request.POST.getlist('maj1')
        maj2s = request.POST.getlist('maj2')
        min1s = request.POST.getlist('min1')
        min2s = request.POST.getlist('min2')
        is_whittiers = request.POST.getlist('is_whittier')
        notes = request.POST.getlist('notes')
        
        for i in range(len(subjs)):
            subj = subjs[i]
            num = nums[i]
            title = titles[i]
            term = terms[i]
            year = years[i]
            cr = crs[i]
            crn = crns[i]
            instructor = instructors[i]
            completed = completeds[i]
            maj1 = maj1s[i]
            maj2 = maj2s[i]
            min1 = min1s[i]
            min2 = min2s[i]
            is_whittier = is_whittiers[i]
            note = notes[i]
            
            term = Term.objects.get(code=(year+term))

            if not cr:
                cr = 0

            if int(completed) > 0:
                completed = True
            else:
                completed = False
            
            if int(maj1) > 0:
                maj1 = True
            else:
                maj1 = False

            if int(maj2) > 0:
                maj2 = True
            else:
                maj2 = False

            if int(min1) > 0:
                min1 = True
            else:
                min1 = False

            if int(min2) > 0:
                min2 = True
            else:
                min2 = False

            if int(is_whittier) > 0:
                is_whittier = True
            else:
                is_whittier = False

            if (subj and num and title and term):
                #look into getobjector404
                course = Course.objects.get(subject__short = subj,
                                            number = num,
                                            title = title,
                                           )

                newedc = EDCourse.objects.create(student = user, 
                                                 course = course,
                                                 term = term, 
                                                 credits = cr,
                                                 completed = completed,
                                                 instructor = instructor, 
                                                 maj1 = maj1,
                                                 maj2 = maj2, 
                                                 min1 = min1,
                                                 min2 = min2,
                                                 is_whittier = is_whittier,
                                                 notes = note,
                                                )
                if crn.isdigit():
                    newedc.crn = crn
                #some checking maybe?
                newedc.save()
        return redirect(reverse('AddCourse'))
    return redirect(reverse('Index'))

#Gets EDCourse object to be deleted and handles error if DNE
@login_required
def DeleteEDCourse(request):

    if request.method == 'POST':
        try:
            course = EDCourse.objects.get(student=request.user,
                                          id=request.POST.get('course_id'),
                                         )
            course.delete()
            return redirect(reverse('CourseList'))

        except EDCourse.DoesNotExist:
            return redirect(reverse('Index'))

            return redirect(request.META['HTTP_REFERER'])
