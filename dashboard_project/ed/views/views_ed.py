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

import logging
logger = logging.getLogger(__name__)

try:
    hero = HeroImage.objects.get(app='ed')
#except HeroImage.DoesNotExist:
#    hero = HeroImage.objects.get(app='default')
except:
    hero = None

#contains links to other parts of the site and welcomes user

def EDIndex(request):

    council = 0
    staff = 0
    student = 0
    usrgrps = request.user.groups.all()
    for grp in usrgrps:
        if grp.name == 'Council':
            council = 1
        elif grp.name == 'Staff':
            staff = 1
        elif grp.name == 'Student':
            student = 1

    return render(request, 'ed/landingpage.html', 
                          {'pagename': "Welcome",
                           'council': council,
                           'staff': staff,
                           'student': student,
                           'name': request.user.username,
                           'hero': hero,
                          }
           )

#Displays statistics for divisions, departments, and subjects
def Stats(request):

    usrgrp = request.user.groups.all()
    total = Course.numcourses()

    divisions = Division.objects.all()
    divcounts = []
    divpercent = []
    for div in divisions:
        divcounts.append(div.numcourses())
        divpercent.append(div.perccourses())

    departments = Department.objects.all()
    deptcounts = []
    deptpercent = []
    for dept in departments:
        deptcounts.append(dept.numcourses())
        deptpercent.append(dept.perccourses())

    subjects = Subject.objects.all()
    subjcounts = []
    subjpercent = []
    for subj in subjects:
        subjcounts.append(subj.numcourses())
        subjpercent.append(subj.perccourses())

    return render(request, 'ed/stats.html', {"pagename": "Stats",
                                             'total': total,
                                             'divisions': divisions,
                                             'divcounts': divcounts,
                                             'divpercent': divpercent,
                                             'departments': departments,
                                             'deptcounts': deptcounts,
                                             'deptpercent': deptpercent,
                                             'subjects': subjects,
                                             'subjcounts': subjcounts,
                                             'subjpercent': subjpercent,
                                             'hero': hero,
                                            }
                 )

#Page to let user log in to account to access more parts of the site
def WSPLogin(request):

    return render(request, 'edbase.html', {"pagename": "Login Page"})

#JavaScript API for AddEDCourse page
#use parent or div thing with js in template
#to ensure that you won't populate other forms while changing the dropdown
@login_required
def API(request, subj='', num=''):
    
    user = request.user
    if request.method == 'GET':
        if subj:
            if num:
                #send back titles
                qset_titles = Course.objects.filter(number = num, 
                                                    subject__short = subj)
                titles_dict = {c.title: c.number for c in qset_titles if c.title != 'undefined'}
                return JsonResponse(titles_dict)
            else:
                #subject given but not number
                qset = Course.objects.filter(subject__short = subj)
                num_dict = {c.number: c.number for c in qset}
                return JsonResponse(num_dict)
        else:
            if num:
                #number given but not subj, likely malicious
                HttpResponseRedirect(reverse('Index'))
            #no subj and no num, return json of subjects
            return JsonResponse([], safe=False)

@login_required
def ED(request, username=None):
    user = request.user
    
    if request.method == 'POST':
        if is_WSPstaff(user) or is_council(user):
            try:
                student = User.objects.get(id=request.POST.get('student'))
            except User.DoesNotExist:
                return redirect(reverse('ED'))
            return redirect(reverse('ED')+student.username)
        else:
            return redirect(reverse('Index'))
    
    elif request.method == 'GET':
        if is_student(user):
            username = request.user.username
            edgoals = EducationalGoal.objects.filter(student=user)
            studentcourses = all_courses(user)
            divcourses = courses_by_division(user)
            major1 = major_courses(user, 1)
            major2 = major_courses(user, 2)
            minor1 = minor_courses(user, 1)
            minor2 = minor_courses(user, 2)
            wspcourses = WSPcourses(user)
            support = supporting_courses(user)
            
            try:
                student = Student.objects.get(user=user)
                narrative = student.narrative
            except Student.DoesNotExist:
                narrative = ""
            
            return render(request, 'ed/ED.html',
                                  {'user': user,
                                   'username': username,
                                   'usercourses': studentcourses,
                                   'divcourses': divcourses,
                                   'major1': major1,
                                   'major2': major2,
                                   'minor1': minor1,
                                   'minor2': minor2,
                                   'wspcourses': wspcourses,
                                   'support': support,
                                   'edgoals': edgoals,
                                   'narrative': narrative,
                                   'pagename': "Educational Design",
                                   'hero': hero,
                                  }
                         )
        elif is_WSPstaff(user) or is_council(user):
            if username is None:
                studentlist = all_students()
                return render(request, 'ed/studentpickerform.html',
                                       {'pagename': 'Select Student',
                                        'students': studentlist,
                                        'target': 'ED',
                                        'hero': hero,
                                       }
                             )
            else:
                # Setting up the table
                student = User.objects.get(username=username)
                edgoals = EducationalGoal.objects.filter(student=student)
                studentcourses = all_courses(student)
                divcourses = courses_by_division(student)
                major1 = major_courses(student, 1)
                major2 = major_courses(student, 2)
                minor1 = minor_courses(student, 1)
                minor2 = minor_courses(student, 2)
                wspcourses = WSPcourses(student)
                support = supporting_courses(student)   
                
                # setting up the form
                
                try:
                    student_obj = Student.objects.get(user=student)
                    narrative = student_obj.narrative
                except Student.DoesNotExist:
                    narrative = ""
                pagename = student.get_full_name() + " Educational Design"
                return render(request, 'ed/ED.html',
                                      {'user': student,
                                       'username': username,
                                       'usercourses': studentcourses,
                                       'divcourses': divcourses,
                                       'major1': major1,
                                       'major2': major2,
                                       'minor1': minor1,
                                       'minor2': minor2,
                                       'wspcourses': wspcourses,
                                       'support': support,
                                       'edgoals': edgoals,
                                       'narrative': narrative,
                                       'pagename': pagename,
                                       'hero': hero,
                                      }
                             )
        else:
            return redirect(reverse('Index'))
    else:
        return redirect(reverse('Index'))

# copies  current ED into approved ED
@login_required
def ApproveED(request):
    user = request.user
    #try:
    if request.method == 'POST':
        if is_WSPstaff(user):
            username = request.POST.get('student')
            student = User.objects.get(username=username)
            ED = all_courses(student)
            
            #Updates the approved status of every course
            for course in ED:
                checkmark = request.POST.get('%(course)s' % {'course': course,}) #I had to use a c like pritf statment to make this work
                if checkmark:
                    course.approved = True
                else:
                    course.approved = False
                course.save()
            
            approved = ED.filter(approved=True)

            #Removes old courses that are not in the new course list
            oldApproved = approved_courses(student)
            for c in oldApproved:
                if approved.filter(course=c.course).exists() == False:
                    c.delete()
            
            # Adds new courses to Approved Course list
            for course in approved:
                # checks is Approved course already exists. If it does, update it. If it does not, create a new one.
                
                edcourseID = course.id
                if oldApproved.filter(course=course.course, student=student).exists():
                #if oldApproved.filter(edcourseID=edcourseID).exists():
                    term = course.term
                    credits = course.credits
                    completed = course.completed
                    crn = course.crn
                    instructor = course.instructor
                    maj1 = course.maj1
                    maj2 = course.maj2
                    min1 = course.min1
                    min2 = course.min2
                    is_whittier = course.is_whittier
                    notes = course.notes

                    update = ApprovedCourse.objects.get(course=course.course, student=student)
                    #update = ApprovedCourse.objects.get(edcourseID=edcourseID)
                    update.term = term
                    update.credits = credits
                    update.completed = completed
                    update.crn = crn
                    update.instructor = instructor
                    update.maj1 = maj1
                    update.maj2 = maj2
                    update.min1 = min1
                    update.min2 = min2
                    update.is_whittier = is_whittier
                    update.notes = notes
                    update.save() 

                else:
                    approveddcourse = ApprovedCourse(student = student,
                                                    course = course.course,
                                                    term = course.term,
                                                    credits = course.credits,
                                                    completed = course.completed,
                                                    crn = course.crn,
                                                    instructor = course.instructor,
                                                    maj1 = course.maj1,
                                                    maj2 = course.maj2,
                                                    min1 = course.min1,
                                                    min2 = course.min2,
                                                    is_whittier = course.is_whittier,
                                                    notes =  course.notes,
                                                    edcourseID = edcourseID,
                                        )
                    approveddcourse.save()
            
            #Sets EDmeeting_complte to true
            vitaStudent = Student.objects.get(user=student)
            vitaStudent.EDmeeting_complete = True
            vitaStudent.save()

            return HttpResponseRedirect(reverse('ApprovedCourses')+student.username) 
    else:
        return HttpResponseRedirect(reverse('Index'))
    #except:
    #    return HttpResponseRedirect(reverse('Index'))
