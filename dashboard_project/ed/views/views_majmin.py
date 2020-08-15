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
def MajorMinor(request):
    user = request.user

    if request.method == 'GET':
        if is_student(user):
            studentcourses = all_courses(user)
            major1 = major_courses(user, 1)
            major2 = major_courses(user, 2)
            minor1 = minor_courses(user, 1)
            minor2 = minor_courses(user, 2)
            return render(
                request,
                'ed/MajorMinorForm.html',
                {
                    'pagename': "Major/Minor",
                    'major1': major1,
                    'major2': major2,
                    'minor1': minor1,
                    'minor2': minor2,
                    'usercourses': studentcourses,
                    'hero': hero,
                }
            )
        else:
            return HttpResponseRedirect(reverse('Index'))

    elif request.method == 'POST':
        if not is_student(user):
            return HttpResponseRedirect(reverse('Index'))

        maj1 = None
        maj2 = None
        min1 = None
        min2 = None

        try:
            maj1 = Major.objects.get(student=user, number=1)
        except Major.DoesNotExist:
            pass
        try:
            maj2 = Major.objects.get(student=user, number=2)
        except Major.DoesNotExist:
            pass
        try:
            min1 = Minor.objects.get(student=user, number=1)
        except Minor.DoesNotExist:
            pass
        try:
            min2 = Minor.objects.get(student=user, number=2)
        except Minor.DoesNotExist:
            pass

        studentgroup = Group.objects.get(name='student')
        student = False
        for group in user.groups.all():
            if group == studentgroup:
                student = True
        if student:
            title1 = request.POST.get('maj1title')
            sum1 = request.POST.get('maj1summary')
            title2 = request.POST.get('maj2title')
            sum2 = request.POST.get('maj2summary')
            title3 = request.POST.get('min1title')
            sum3 = request.POST.get('min1summary')
            title4 = request.POST.get('min2title')
            sum4 = request.POST.get('min2summary')

            if maj1:
                maj1.student = user
                maj1.title = title1
                maj1.description = sum1
                maj1.number = 1
                maj1.save()
            else:
                if title1:
                    maj1 = Major.objects.create(
                        student=user,
                        title=title1,
                        description=sum1,
                        number=1
                    )
                    maj1.save()
            if maj2:
                maj2.student = user
                maj2.title = title2
                maj2.description = sum2
                maj2.number = 2
                maj2.save()
            else:
                if title2:
                    maj2 = Major.objects.create(
                        student=user,
                        title=title2,
                        description=sum2,
                        number=2
                    )
                    maj2.save()
            if min1:
                min1.student = user
                min1.title = title3
                min1.description = sum3
                min1.number = 1
                min1.save()
            else:
                if title3:
                    min1 = Minor.objects.create(
                        student=user,
                        title=title3,
                        description=sum3,
                        number=1
                    )
                    min1.save()
            if min2:
                min2.student = user
                min2.title = title4
                min2.description = sum4
                min2.number = 2
                min2.save()
            else:
                if title4:
                    min2 = Minor.objects.create(
                        student=user,
                        title=title4,
                        description=sum4,
                        number=2
                    )
                    min2.save()

            user = request.user
            major1 = major_courses(user, 1)
            major2 = major_courses(user, 2)
            minor1 = minor_courses(user, 1)
            minor2 = minor_courses(user, 2)

            studentcourses = all_courses(user)
            return render(
                request,
                'ed/MajorMinorForm.html',
                {
                    'pagename': "Major/Minor",
                    'major1': major1,
                    'major2': major2,
                    'minor1': minor1,
                    'minor2': minor2,
                    'usercourses': studentcourses,
                    'hero': hero,
                }
            )

        else:
            return HttpResponseRedirect(reverse('Index'))
    else:
        return HttpResponseRedirect(reverse('Index'))


@login_required
def DeleteMajor(request):
    if request.method == 'POST':
        try:
            user = request.user
            major_id = int(request.POST.get('major_id'))
            courselist = major_courses(user, major_id)
        except Major.DoesNotExist:
            return HttpResponseRedirect(reverse('Index'))

        for course in courselist:
            if major_id == 1:
                course.maj1 = False
                course.save()
            if major_id == 2:
                course.maj2 = False
                course.save()
        major = Major.objects.get(student=user, number=major_id)
        major.delete()
        return HttpResponseRedirect(reverse('CourseList'))


@login_required
def DeleteMinor(request):
    if request.method == 'POST':
        try:
            user = request.user
            minor_id = int(request.POST.get('minor_id'))
            courselist = minor_courses(user, minor_id)
        except Minor.DoesNotExist:
            return HttpResponseRedirect(reverse('Index'))

        for course in courselist:
            if minor_id == 1:
                course.min1 = False
                course.save()
            if minor_id == 2:
                course.min2 = False
                course.save()
        minor = Minor.objects.get(student=user, number=minor_id)
        minor.delete()
        return HttpResponseRedirect(reverse('CourseList'))
