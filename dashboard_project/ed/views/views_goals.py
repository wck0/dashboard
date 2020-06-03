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

#deletes EducationalGoal object
@login_required
def DeleteEducationalGoal(request):
    if request.method == 'POST':
        try:
            delobj = EducationalGoal.objects.get(
                        student=request.user,
                        id=request.POST.get('egoal_id'),
                     )
            delobj.delete()
            return HttpResponseRedirect(reverse('AddGoal'))

        except EducationalGoal.DoesNotExist:
            return HttpResponseRedirect(reverse('Index'))
    else:
        return HttpResponseRedirect(reverse('Index'))

@login_required
def Goals(request):
    user = request.user
    edgoals = EducationalGoal.objects.filter(student=user)
    
    if request.method == 'GET':
        
        return render(request, 'ed/allgoals.html',
                              {'edgoals': edgoals,
                               'pagename': 'Your Educational Goals',
                               'hero': hero,
                              }
                     )

#Use poefolio as reference
@login_required
def AddEducationalGoal(request):
    user = request.user
    form = EducationalGoalForm(user=user)
#    form.fields['courses'].queryset = EDCourse.objects.filter(student=request.user)
    
    if request.method == 'GET':
        edgoals = EducationalGoal.objects.filter(student=user)

        return render(request, 'ed/EducationalGoalForm.html',
                              {'edgoals': edgoals,
#                               'courses': studentcourses,
                               'pagename': 'Your Educational Goals',
                               'form': form,
                               'hero': hero,
                              }
                     )

    elif request.method == 'POST':
        form = EducationalGoalForm(request.POST, user=user)
        
        if form.is_valid():
            goal = form.save(commit=False)
            goal.student = request.user
            goal.save()
            goal.courses.set(form.cleaned_data.get('courses'))
            form.save_m2m()
            
        
        return HttpResponseRedirect(reverse('AddGoal'))

    else:
        return HttpResponseRedirect(reverse('Index'))

@login_required
def EditEDGoal(request, goal_id=None):
    user = request.user
    edgoal = EducationalGoal.objects.get(id=goal_id)
    if (request.method == 'GET') and (user == edgoal.student):
        form = EducationalGoalForm(user=user)
        form.fields['title'].initial = edgoal.title
        form.fields['description'].initial = edgoal.description
        
        course_id = [] # creates a list of couse id's and uses them to define which boxes get checked
        for course in edgoal.courses.all():
            course_id.append(course.id)
        form.fields['courses'].initial = course_id
       
        return render(request, 'ed/editgoal.html',
                              {'edgoal':edgoal,
                               'form':form,
                               'pagename':'Edit Goal',
                               'hero': hero,
                              }
                     )
    elif (request.method == 'POST') and (user == edgoal.student):
        form = EducationalGoalForm(request.POST or None,
                                   instance=edgoal,
                                   user=user,)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse('AllGoals'))
    else:
        return HttpResponseRedirect(reverse('EDIndex'))
