import datetime
from vita.models import *
from vita.forms import *
from ed.tools import *
from poetfolio.tools import *
from siteconfig.models import HeroImage
from django.urls import reverse
from django.views import generic
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.mail import EmailMessage

import logging
logger = logging.getLogger(__name__)

try:
    hero = HeroImage.objects.get(app='vita')
#except HeroImage.DoesNotExist:
#    hero = HeroImage.objects.get(app='default')
except:
    hero = None

@login_required
def Index(request):
    user = request.user
    if is_student(user):
        try:
            Student.objects.get(user=user)
        except Student.DoesNotExist:
            student = Student.objects.create(user=user)
        
        try:
            Application.objects.get(user=user)
        except Application.DoesNotExist:
            application = Application.objects.create(user=user)
    
    return render(request, 'vitabase.html',
                  {'pagename':'Vita',
                   'hero': hero,
                  }
                 )

@login_required
def Narrative(request):
    if request.method == 'GET':
        if is_student(request.user):
            student = Student.objects.get(user=request.user)
            return render(request, 'vita/narrative.html',
                          {'pagename':request.user.username + "'s Proposal",
                           'narrative': student.narrative,
                           'hero': hero,
                          }
                         )
        else:
            return redirect(reverse('VitaApplication'))
    elif request.method == 'POST':
        if is_student(request.user):
            student = Student.objects.get(user=request.user)
            form = StudentNarrativeForm(request.POST, instance=student)
            if form.is_valid():
                form.save()
            return redirect(reverse('VitaNarrative'))
        else:
            return redirect(reverse('VitaApplication'))

@login_required
def EditNarrative(request):
    student = Student.objects.get(user=request.user)
    form = StudentNarrativeForm()
    form.fields['narrative'].initial = student.narrative
    return render(request, 'vita/editnarrative.html',
                  {'pagename': 'Edit Narrative',
                   'form': form,
                   'narrative': student.narrative,
                   'hero': hero,
                  }
                 )

@login_required
def Info(request, username=None):
    user = request.user
    if is_student(user):
        if username is not None:
            return redirect(reverse('VitaInfo'))
        if request.method == 'GET':
     
            student = Student.objects.get(user=user)
            form = StudentInfoForm(instance=student)
            if student.phone:
                form['phone'].initial = student.phone.as_national
            return render(request, 'vita/info.html',
                          {'pagename': 'Your Info',
                           'user': user,
                           'form': form,
                           'hero': hero,
                          }
                         )
        elif request.method == 'POST':
            student = Student.objects.get(user=user)
            form = StudentInfoForm(request.POST, instance=student)
            if form.is_valid():
                form.save()
                return redirect(reverse('VitaInfo'))
            else:
                return render(request, 'vita/info.html',
                      {'pagename': 'Your Info',
                       'form': form,
                       'hero': hero,
                      }
                     )
        else:
            return redirect(reverse('VitaIndex'))
    elif is_council(user) or is_WSPstaff(user):
        if request.method == 'GET':
            if username is None:
                students = all_students()
                return render(request, 'vita/studentpickerform.html',
                              {'pagename': 'Student Info',
                               'target': 'VitaInfo',
                               'students': students,
                               'hero': hero,
                              }
                             )
            else:
                user = User.objects.get(username=username)
                student = Student.objects.get(user=user)
                return render(request, 'vita/viewinfo.html',
                              {'pagename': user.get_full_name(),
                               'user': user,
                               'student': student,
                               'hero': hero,
                              }
                             )
        elif request.method == 'POST':
            user_id = request.POST.get('student')
            user = User.objects.get(id=user_id)
            return redirect(reverse('VitaInfo')+user.username)
    else:
        return redirect(reverse('VitaIndex'))

@login_required
def ApplicationView(request, username=None):
    user = request.user
    if is_student(user):
        if username:
            return redirect(reverse('VitaApplication'))
        if request.method == 'GET':
            try:
                student = Student.objects.get(user=user)
            except Student.DoesNotExist:
                return redirect(reverse('VitaIndex'))
            infoform = StudentInfoForm(instance=student)
            app = Application.objects.get(user=user)
            appform = ApplicationForm(instance=app)
            if student.phone:
                infoform['phone'].initial = student.phone.as_national
            
            usercourses = all_courses(user)
        
            return render(request, 'vita/application.html',
                          {'pagename': 'Your Application to WSP',
                           'appform': appform,
                           'infoform': infoform,
                           'user': user,
                           'usercourses': usercourses,
                           'application': app,
                           'hero': hero,
                          }
                         )
        elif request.method == 'POST':
            try:
                student = Student.objects.get(user=user)
            except Student.DoesNotExist:
                return redirect(reverse('VitaIndex'))
            action = request.POST.get('action')
            if action == 'save':
                app = Application.objects.get(user=user)
                form = ApplicationForm(request.POST, instance=app)
                if form.is_valid():
                    form.save()
                form = StudentInfoForm(request.POST, instance=student)
                if form.is_valid():
                    form.save()
                return redirect(reverse('VitaApplication'))
            elif action == 'submit':
                app = Application.objects.get(user=user)
                form = ApplicationForm(request.POST, instance=app)
                if form.is_valid():
                    form.save()
                    app = Application.objects.get(user=user)
                    app.submitted = True
                    app.resubmit = False
                    app.last_submitted = datetime.datetime.now()
                    app.save()
                form = StudentInfoForm(request.POST, instance=student)
                if form.is_valid():
                    form.save()
                    subj = 'WSP Application Submitted'
                    body = "Dear " + student.user.get_full_name() + ",\n" 
                    body += "Your application has been submitted, and your application essay is bellow.\n"
                    body += "Sincerely,\n The Whittier Scholars Program\n\n"
                    body += app.essay 
                    sender = 'scholars@whittier.edu'
                    receiver = [student.user.email]
                    
                    email = EmailMessage (subj, body, sender, receiver, cc = [sender])
                    email.send()
                return redirect(reverse('VitaApplication'))
        else:
            return redirect(reverse('VitaIndex'))
    if is_council(user) or is_WSPstaff(user):
        if request.method == 'GET':
            if username is None:
                now = datetime.datetime.now()
                timewindow = datetime.timedelta(days=90)
                apps = Application.objects.filter(submitted=True,
                                                 last_submitted__gte=(now-timewindow),
                                                 ).order_by('user__last_name')
                return render(request, 'vita/viewapplications.html',
                              {'pagename': 'Applications',
                               'applications': apps,
                               'hero': hero,
                              }
                             )
            else:
                try:
                    app = Application.objects.get(user__username=username)
                    student = User.objects.get(username=username)
                    courses = all_courses(student)
                    if is_WSPstaff(user):
                        buttons = True
                        form = ApplicationFeedbackForm(instance=app)
                    else:
                        buttons = False
                        form = None
                    return render(request, 'vita/singleapplication.html',
                                  {'pagename': 'Application',
                                   'application': app,
                                   'usercourses': courses,
                                   'buttons':buttons,
                                   'form':form,
                                   'hero': hero,
                                  }
                                 )
                except Application.DoesNotExist:
                    return redirect(reverse('VitaApplication'))
    if is_WSPstaff(user) and request.method == 'POST':
        if username is None:
            return redirect(reverse('VitaApplication'))
        else:
            try:
                app = Application.objects.get(user__username=username)
                student = User.objects.get(username=username)
                action = request.POST.get('action')
                if action == 'accept':
                    app.rejected = False
                    app.accepted = True
                    app.save()
                elif action == 'revise':
                    app.rejected = False
                    app.accepted = False
                    app.resubmit = True
                    app.save()
                elif action == 'reject':
                    app.rejected = True
                    app.accepted = False
                    app.save()
                elif action =='save':
                    form = ApplicationFeedbackForm(request.POST, instance=app)
                    if form.is_valid():
                        form.save()
                    return HttpResponseRedirect(request.path_info)
            except Application.DoesNotExist:
                return redirect(reverse('VitaApplication'))
        return redirect(reverse('VitaApplication'))

@login_required
def OffCampus(request, username=None):
    user = request.user
    if is_student(user):
        if username:
            return redirect(reverse('VitaOffCampus'))
        if request.method == 'GET':
            try:
                student = Student.objects.get(user=user)
            except Student.DoesNotExist:
                return redirect(reverse('VitaIndex'))
            
            exp = OffCampusExperience.objects.get(user=user)
            expform = OffCampusReflectForm(instance=exp)

            return render(request, 'vita/offcampus.html',
                          {'pagename': 'Your Off Campus Experience',
                           'exp': exp,
                           'expform': expform,
                           'user': user,
                           'hero': hero,
                          }
                         )
        elif request.method == 'POST':
            try:
                student = Student.objects.get(user=user)
            except Student.DoesNotExist:
                return redirect(reverse('VitaIndex'))

            exp = OffCampusExperience.objects.get(user=user)
            
            form = OffCampusReflectForm(request.POST, instance=exp)
            if form.is_valid():
                form.save()
            
            return redirect(reverse('VitaOffCampus'))
    
    elif is_council(user) or is_WSPstaff(user):
        if request.method == 'GET':
            if username is None:
                students = all_students()
                return render(request, 'vita/studentpickerform.html',
                              {'pagename': 'Off Campus Experience',
                               'target': 'VitaOffCampus',
                               'students': students,
                               'hero': hero,
                              }
                             )
            else:
                user = User.objects.get(username=username)
                student = Student.objects.get(user=user)

                exp = OffCampusExperience.objects.get(user=user)
                notesForm = OffCampusCouncilNotesForm(instance=exp)
                expType = exp.get_experince_type_display()
                print("The user  is: ", user)
                
                return render(request, 'vita/offcampus.html',
                              {'pagename': 'Off Campus Experience',
                               'exp': exp, 
                               'notesForm': notesForm,
                               'expType': expType,
                               'user': user,
                               'student': student,
                               'hero': hero,
                              }
                             )
            
        elif request.method == 'POST':

            #checks if the post is coming from the button or the student picker
            student_user = request.POST.get('submit')
            if student_user:
                user = User.objects.get(username=student_user)
                
                exp = OffCampusExperience.objects.get(user=user)
                form = OffCampusCouncilNotesForm(request.POST, instance=exp)
                if form.is_valid():
                    form.save()
            # post is coming from student picker 
            else: 
                user_id = request.POST.get('student')
                user = User.objects.get(id=user_id)

            
            return redirect(reverse('VitaOffCampus')+user.username)
            
            
    else:
        return redirect(reverse('VitaIndex'))
