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
except HeroImage.DoesNotExist:
    hero = None

@login_required
def ApprovedCourseList(request, username=None):
    user = request.user

    if request.method == 'POST':
        if is_WSPstaff(user) or is_council(user):
            try:
                student = User.objects.get(id=request.POST.get('student'))
            except User.DoesNotExist:
                return redirect(reverse('ApprovedCourses'))

            return redirect(reverse('ApprovedCourses')+student.username)

        else:
            return redirect(reverse('Index'))

    elif request.method == 'GET':
        if is_student(user):
            approvedcourses = approved_courses(user)
            ED = all_courses(user)

            removedcourses = approvedcourses
            for c in ED:
                removedcourses = removedcourses.exclude(course=c.course)

            newcourses = ED
            for c in approvedcourses:
                newcourses = newcourses.exclude(course=c.course)

            return render(
                request,
                'ed/approvedcourses.html',
                {
                    'pagename': 'Filed Design',
                    'user': user,
                    'usercourses': approvedcourses,
                    'removedcourses': removedcourses,
                    'newcourses': newcourses,
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
                        'target': 'ApprovedCourses',
                        'hero': hero,
                    }
                )
            else:
                student = User.objects.get(username=username)
                approvedcourses = approved_courses(student)
                ED = all_courses(student)
                removedcourses = approvedcourses
                for course in ED:
                    removedcourses = removedcourses.exclude(
                        course=course.course
                    )
                newcourses = ED
                for c in approvedcourses:
                    newcourses = newcourses.exclude(course=c.course)

                pagename = f"{student.get_full_name()} Approved Course list"
                return render(
                    request,
                    'ed/approvedcourses.html',
                    {
                        'pagename': pagename,
                        'user': student,
                        'usercourses': approvedcourses,
                        'removedcourses': removedcourses,
                        'newcourses': newcourses,
                        'hero': hero,
                    }
                )

        else:
            return redirect(reverse('Index'))
    else:
        return redirect(reverse('Index'))


@login_required
def ReplaceAppCourse(request, appcourse_id=None):
    user = request.user
    if not is_student(user):
        return redirect(reverse('Index'))

    if request.method == 'GET':
        if appcourse_id:
            try:
                appcourse = ApprovedCourse.objects.get(
                    student=user,
                    id=appcourse_id,
                )
            except ApprovedCourse.DoesNotExist:
                return redirect(reverse('Index'))

            newcourses = all_courses(user)
            for c in ApprovedCourse.objects.filter(student=user):
                newcourses = newcourses.exclude(course=c.course)

            return render(
                request,
                'ed/replaceAppcourse.html',
                {
                    'pagename': 'Edit Course',
                    'user': user,
                    'appcourse': appcourse,
                    'newcourses': newcourses,
                    'hero': hero,
                }
            )
        else:
            return render(request, 'ed/editEDCourse.html', {})

    elif (appcourse_id is not None) and (request.method == 'POST'):
        try:
            replacement_id = request.POST.get('replacement')
            reason = request.POST.get('reason')

            appcourse = ApprovedCourse.objects.get(id=appcourse_id)
            replacement = EDCourse.objects.get(id=replacement_id)

            if appcourse.student == user:
                appcourse.replacement = replacement
                appcourse.reason = reason
                appcourse.save()
                return redirect(reverse('ApprovedCourses'))
            else:
                return redirect(reverse('Index'))
        except KeyError:
            return redirect(reverse('ApprovedCourses'))
        except ApprovedCourse.DoesNotExist:
            return redirect(reverse('ApprovedCourses'))
        except EDCourse.DoesNotExist:
            return redirect(reverse('ApprovedCourses'))

    return redirect(reverse('Index'))


def ApproveAppCourseReplacement(request):
    user = request.user
    if is_student(user):
        return redirect(reverse('Index'))

    if request.method == 'POST':
        replace = request.POST.get('replace')
        student = request.POST.get('student')
        course_id = int(request.POST.get('course_id'))

        if replace:
            oldcourse = ApprovedCourse.objects.get(id=course_id)

            try:
                newcourse_id = request.POST.get('newcourse_id')
                newcourse = EDCourse.objects.get(id=newcourse_id)

                approveddcourse = ApprovedCourse(
                    student=newcourse.student,
                    course=newcourse.course,
                    term=newcourse.term,
                    credits=newcourse.credits,
                    completed=newcourse.completed,
                    crn=newcourse.crn,
                    instructor=newcourse.instructor,
                    maj1=newcourse.maj1,
                    maj2=newcourse.maj2,
                    min1=newcourse.min1,
                    min2=newcourse.min2,
                    is_whittier=newcourse.is_whittier,
                    notes=newcourse.notes,
                )
                approveddcourse.save()
            except KeyError:
                pass
            except EDCourse.DoesNotExist:
                pass
            finally:
                oldcourse.delete()

            return redirect(request.META['HTTP_REFERER'])
        else:
            newcourse = EDCourse.objects.get(id=course_id)
            approveddcourse = ApprovedCourse(
                student=newcourse.student,
                course=newcourse.course,
                term=newcourse.term,
                credits=newcourse.credits,
                completed=newcourse.completed,
                crn=newcourse.crn,
                instructor=newcourse.instructor,
                maj1=newcourse.maj1,
                maj2=newcourse.maj2,
                min1=newcourse.min1,
                min2=newcourse.min2,
                is_whittier=newcourse.is_whittier,
                notes=newcourse.notes,
            )
            approveddcourse.save()
