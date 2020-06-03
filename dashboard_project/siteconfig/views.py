from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import StudentsForm 
from scripts.users.import_students import import_students
import subprocess
# Create your views here.

# TODO: restrict EnterStudents to the appropriate group.

# StudentsForm is the from from forms.py
# import_students is the script from /scripts/users that does the registration
@login_required
def EnterStudents(request):
    if request.method == 'POST':
        form = StudentsForm(request.POST, request.FILES)
        
        #using the os to check the file type
        upload = request.FILES['file'].temporary_file_path()        
        temp_file = subprocess.check_output(['file', '-bi', upload]) #in console: $ file -bi upload
        temp_file = str(temp_file[0:28].decode()) 
 
        #checks if tables are full and if file is a plain text doc
        if form.is_valid and temp_file == "text/plain; charset=us-ascii":
            submitted = import_students(request.FILES['file']) # runs the import_students function from import_students.py
            return render(request, 'siteconfig/SuccessSubmit.html', {'submitted': submitted})
        else:
            subprocess.Popen(['rm', upload]) #deletes files that get rejected so they can't be run
            error = True #rasies in error if the submission is the wrong file type
    else:
        form = StudentsForm()
        error = False
    return render(request, 'siteconfig/EnterStudents.html', {'form': form,
                                                             'error': error,
                                                            })    
