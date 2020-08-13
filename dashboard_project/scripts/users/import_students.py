# make sure the appropriate venv is activated
# before running this script

# navigate to manage.py in a terminal
# activate the appropriate venv
# ./manage.py shell < path/to/this/script.py

import csv
from django.contrib.auth.models import User, Group
from vita.models import Student, Application
from ed.models import Course, EDCourse, ApprovedCourse
from siteconfig.models import RequiredCourses



def add_course(course, new_user):
    edcourse = EDCourse(student = new_user, 
                        course = course.course, 
                        credits = course.credits
                        )
    edcourse.save()

def import_students(student_list):
    # sets up the group we'll put the new user in
    student_group = Group.objects.get(name="Student")

    # List of students to be returned when they are entered correctly
    submit_list = []

    # Defines the row headers that the fuction will look will look for
    FIRST = "First name"
    LAST = "Last name"
    EMAIL = "Email address"

    tempfile = student_list.temporary_file_path()
    with open(tempfile, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # checks if the fields are valid
            try:
                first_name = row[FIRST]
            except:
                submit_list.append("Error adding student")
            
            try:
                last_name = row[LAST]
                email = row[EMAIL]
                at_index = email.index('@')
                username = email[:at_index]
            except:
                submit_list.append("Error adding " + first_name)
                
            #Checks if student already exists
            try:
                existing_user = User.objects.get(username=username)
                existing_student = 'user ' + username + ' already exists'
                submit_list.append(existing_student) # append a list of students who's accounts already exist
            
            # Adds new student
            except User.DoesNotExist:
                new_user = User(first_name=first_name,
                                last_name=last_name,
                                email=email,
                                username=username,
                               )
                new_user.save()
                new_user.groups.add(student_group)
                new_user.save()
                new_student = Student(user=new_user)
                new_student.save() 
                new_app = Application(user=new_user) #Causes that weird null object erros
                new_app.save()
                new_offCampus = OffCampusExperience(user=new_user)
                new_offCampus.save()
                
                #Adding classes
                for course in RequiredCourses.objects.all():
                    add_course(course, new_user)
                
                # lock WSP classes
                new_student = "New user " + username + " " + "(" + first_name + " " + last_name + ")"
                submit_list.append(new_student)
    
    submit_list.sort()
    return submit_list
