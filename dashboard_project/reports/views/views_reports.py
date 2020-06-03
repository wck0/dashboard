from poetfolio.tools import *
from ed.models import *
from ed.forms import *
from ed.tools import *
from siteconfig.models import HeroImage
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required

try:
    hero = HeroImage.objects.get(app='reports')
#except HeroImage.DoesNotExist:
#    hero = HeroImage.objects.get(app='default')
except:
    hero = None

def ReportsIndex(request, username=None):
    user = request.user
    
    if request.method == 'GET':
        if is_student(request.user):
            studentcourses = all_courses(user)
            major1 = major_courses(user, 1)
            major2 = major_courses(user, 2)
            minor1 = minor_courses(user, 1)
            minor2 = minor_courses(user, 2)
            wspcourses = WSPcourses (user)
            divcourses = courses_by_division(user)
            return render(request, 'reports/reports.html',
                                   {'pagename': request.user.get_full_name(),
                                    'username': request.user.username,
                                    'user': user,
                                    'usercourses': studentcourses,
                                    'divcourses': divcourses,
                                    'wspcourses' : wspcourses,
                                    'major1': major1,
                                    'major2': major2,
                                    'minor1': minor1,
                                    'minor2': minor2,
                                    'hero': hero,
                                   }
                         )
        elif is_WSPstaff(request.user) or is_council(request.user):
            if username is None:
                students = all_students()
                return render(request, 'reports/studentpickerform.html',
                                       {'pagename': 'Reports',
                                        'target': 'ReportsIndex',
                                        'students': students,
                                        'hero': hero,
                                       }
                             )

            else:
                user = User.objects.get(username=username)
                studentcourses = all_courses(user)
                divcourses = courses_by_division(user)
                wspcourses = WSPcourses (user)
                major1 = major_courses(user, 1)
                major2 = major_courses(user, 2)
                minor1 = minor_courses(user, 1)
                minor2 = minor_courses(user, 2)
                return render(request, 'reports/reports.html',
                                       {'pagename': user.get_full_name(),
                                        'username': user.username,
                                        'user': user,
                                        'usercourses': studentcourses,
                                        'divcourses': divcourses,
                                        'wspcourses' : wspcourses,
                                        'major1': major1,
                                        'major2': major2,
                                        'minor1': minor1,
                                        'minor2': minor2,
                                        'hero': hero,
                                       }
                             )
        else:
            return redirect(reverse('Index'))

    elif request.method == 'POST':
        if is_WSPstaff(request.user) or is_council(request.user):
            student_id = request.POST.get('student')
            student = User.objects.get(id=student_id)
            return redirect(reverse('ReportsIndex')+student.username)
        else:
            return redirect(reverse('Index'))
    else:
        return redirect(reverse('Index'))
