from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django import forms
# Create your models here.

# TODO: Switch to f-strings for string formatting.

class Term(models.Model):
    """
    The Registrar's Office refers to terms using a code of the form YYYYMM.
    For the MM part, we have the following convention:
    01 = January
    02 = Spring
    06 = Summer
    09 = Fall
    
    We store this code as an integer, and provide methods for extracting the
    year, semester name, etc.
    """
    code = models.PositiveIntegerField(unique=True)
    
    def year(self):
        return self.code // 100
    
    def month(self):
        return self.code % 100 # integer, so 9 instead of 09, etc.
    
    def name(self):
        m = self.month()
        return {
                1 : 'January',
                2 : 'Spring',
                6 : 'Summer',
                9 : 'Fall',
               }.get(m, '')
    
    def __repr__(self):
        return "<Term %s>" % self.code
    
    def __str__(self):
        return "{} {}".format(self.name(), self.year())

class Division(models.Model):
    """
    These codes are not official college codes. They have been created for
    the poetfolio system's internal reference only.
    
    1 = Humanities
    2 = Natural Sciences
    3 = Social Sciences
    4 = Interdisciplinary
    5 = Non-Academic
    """
    code = models.PositiveSmallIntegerField(unique=True)
    name = models.TextField()

    def numcourses(self):
        return Course.objects.filter(
            subject__department__division = self
        ).count()
    
    def perccourses(self):
        total = Course.numcourses()
        count = Course.objects.filter(
            subject__department__division = self
        ).count()
        
        return ((count/total)*100)

    def __repr__(self):
        return "<Division %s>" % self.name
    
    def __str__(self):
        return self.name

class Department(models.Model):
    name     = models.TextField()
    division = models.ForeignKey(
        Division,
        on_delete=models.CASCADE,
    )

    def numcourses(self):
        return Course.objects.filter(
            subject__department = self
        ).count()

    def perccourses(self):
        total = Course.numcourses()
        count = Course.objects.filter(
            subject__department = self
        ).count()
        
        return ((count/total)*100)

    def __repr__(self):
        return "<Department %s>" % self.name
    
    def __str__(self):
        return self.name

class Subject(models.Model):
    name       = models.TextField()
    short      = models.CharField(max_length=4) # MATH, COSC, etc.
    department = models.ForeignKey(
        Department,
        null=True,
        on_delete=models.SET_NULL,
    )

    def numcourses(self):
        return Course.objects.filter(subject = self).count()

    def perccourses(self):
        total = Course.numcourses()
        count = Course.objects.filter(subject = self).count()
        return ((count/total)*100)

    def __repr__(self):
        return "<Subject %s>" % self.short
    
    def __str__(self):
        return "%s (%s)" % (self.short, self.name)

class Course(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
    )
    number  = models.CharField(max_length=5) # friggin CHEM 110BQ...
    title   = models.TextField()
    active  = models.BooleanField(default=True)
    
    def numcourses():
        return Course.objects.all().count()

    def __repr__(self):
        return "<Course %s %s %s>" % (self.subject.short,
                                      self.number,
                                      self.title
                                     )
    
    def __str__(self):
        return "{} {}".format(self.subject.short,
                              self.number,
                             )

class Major(models.Model):
    student     = models.ForeignKey(User,
                                    on_delete=models.CASCADE,
                                   )
    title       = models.TextField(null=True)
    description = models.TextField(null=True)
    number      = models.PositiveSmallIntegerField()
    

class Minor(models.Model):
    student     = models.ForeignKey(User,
                                    on_delete=models.CASCADE,
                                   )
    title       = models.TextField()
    description = models.TextField()
    number      = models.PositiveSmallIntegerField()    

class EDCourse(models.Model):
    student    = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                  )
    course     = models.ForeignKey(Course,
                                   on_delete=models.CASCADE,
                                  )
    term       = models.ForeignKey(Term,
                                   null=True,
                                   on_delete=models.CASCADE,
                                  )
    credits    = models.FloatField() # transfer courses can have decimal credits
    completed  = models.BooleanField(default=False)
    crn        = models.PositiveIntegerField(null=True)
    instructor = models.TextField(null=True)
    maj1       = models.BooleanField(default=False)
    maj2       = models.BooleanField(default=False)
    min1       = models.BooleanField(default=False)
    min2       = models.BooleanField(default=False)
    is_whittier = models.BooleanField(default=True)
    notes       = models.TextField(blank=True)
    approved    = models.BooleanField(default=True)
   
    def __str__(self):
        the_str = str(self.course) + ": " + self.course.title
        return the_str
    
    def __repr__(self):
        the_repr = str(self.course) + " (" + self.student.username + ")"
        return the_repr


class ApprovedCourse(models.Model):
    student    = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                  )
    course     = models.ForeignKey(Course,
                                   on_delete=models.CASCADE,
                                  )
    term       = models.ForeignKey(Term,
                                   null=True,
                                   on_delete=models.CASCADE,
                                  )
    credits    = models.FloatField() # transfer courses can have decimal credits
    completed  = models.BooleanField(default=False)
    crn        = models.PositiveIntegerField(null=True)
    instructor = models.TextField(null=True)
    maj1       = models.BooleanField(default=False)
    maj2       = models.BooleanField(default=False)
    min1       = models.BooleanField(default=False)
    min2       = models.BooleanField(default=False)
    is_whittier = models.BooleanField(default=True)
    notes       = models.TextField(blank=True)
    replacement = models.ForeignKey(EDCourse,
                                   on_delete=models.CASCADE,
                                   null=True,
                                   blank=True,
                                  )
    reason      = models.TextField(blank=True)
    edcourseID  = models.IntegerField(default=-1)
    
    def __str__(self):
        the_str = str(self.course) + ": " + self.course.title
        return the_str
    
    def __repr__(self):
        the_repr = str(self.course) + " (" + self.student.username + ")"
        return the_repr

class EducationalGoal(models.Model):
    student    = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                  )
    title      = models.CharField(null=True, max_length=80)
    description = models.TextField(null=True)
    courses    = models.ManyToManyField(EDCourse)
    
class EDCourseForm(forms.Form):
    maj1 = forms.BooleanField(required=False)
    maj2 = forms.BooleanField(required=False)
    min1 = forms.BooleanField(required=False)
    min2 = forms.BooleanField(required=False)
    completed = forms.BooleanField(required=False)

