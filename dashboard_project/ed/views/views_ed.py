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
from django.http import JsonResponse

import logging
logger = logging.getLogger(__name__)

try:
    hero = HeroImage.objects.get(app='ed')
except HeroImage.DoesNotExist:
    hero = None


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

    return render(
        request,
        'ed/landingpage.html',
        {
            'pagename': "Welcome",
            'council': council,
            'staff': staff,
            'student': student,
            'name': request.user.username,
            'hero': hero,
        }
    )


@login_required
def API(request, subj='', num=''):

    user = request.user
    if request.method == 'GET':
        if subj:
            if num:
                qset_titles = Course.objects.filter(
                    number=num,
                    subject__short=subj
                )
                titles_dict = {
                    c.title: c.number for c in qset_titles
                    if c.title != 'undefined'
                }
                return JsonResponse(titles_dict)
            else:
                qset = Course.objects.filter(subject__short=subj)
                num_dict = {c.number: c.number for c in qset}
                return JsonResponse(num_dict)
        else:
            if num:
                redirect(reverse('Index'))
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

            return render(
                request,
                'ed/ED.html',
                {
                    'user': user,
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
                return render(
                    request,
                    'ed/studentpickerform.html',
                    {
                        'pagename': 'Select Student',
                        'students': studentlist,
                        'target': 'ED',
                        'hero': hero,
                    }
                )
            else:
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

                try:
                    student_obj = Student.objects.get(user=student)
                    narrative = student_obj.narrative
                except Student.DoesNotExist:
                    narrative = ""
                pagename = student.get_full_name() + " Educational Design"
                return render(
                    request,
                    'ed/ED.html',
                    {
                        'user': student,
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


@login_required
def ApproveED(request):
    user = request.user
    if request.method == 'POST':
        if is_WSPstaff(user):
            username = request.POST.get('student')
            student = User.objects.get(username=username)
            ED = all_courses(student)

            for course in ED:
                checkmark = request.POST.get(f"{course}")
                if checkmark:
                    course.approved = True
                else:
                    course.approved = False
                course.save()

            approved = ED.filter(approved=True)

            oldApproved = approved_courses(student)
            for c in oldApproved:
                if not approved.filter(course=c.course).exists():
                    c.delete()

            for course in approved:
                edcourseID = course.id
#                if oldApproved.filter(edcourseID=edcourseID).exists():
                if oldApproved.filter(
                    course=course.course,
                    student=student
                ).exists():
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

                    update = ApprovedCourse.objects.get(
                        course=course.course,
                        student=student
                    )
#                    update = ApprovedCourse.objects.get(edcourseID=edcourseID)
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
                    approveddcourse = ApprovedCourse(
                        student=student,
                        course=course.course,
                        term=course.term,
                        credits=course.credits,
                        completed=course.completed,
                        crn=course.crn,
                        instructor=course.instructor,
                        maj1=course.maj1,
                        maj2=course.maj2,
                        min1=course.min1,
                        min2=course.min2,
                        is_whittier=course.is_whittier,
                        notes=course.notes,
                        edcourseID=edcourseID,
                    )
                    approveddcourse.save()

            vitaStudent = Student.objects.get(user=student)
            vitaStudent.EDmeeting_complete = True
            vitaStudent.save()

            return redirect(reverse('ApprovedCourses')+student.username)
    else:
        return redirect(reverse('Index'))
