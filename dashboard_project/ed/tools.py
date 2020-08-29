from ed.models import *
from django.db.models import Sum


# some common tools, useful across the site
def calculate_credits(qs):
    aggr = qs.aggregate(Sum('credits'))
    qs.total = aggr.get('credits__sum')

    completed = qs.filter(completed=True)
    aggr = completed.aggregate(Sum('credits'))
    qs.earned = aggr.get('credits__sum')

    return qs


# user courses
def all_courses(user):
    """
    Returns a QuerySet object of all of the user's EDCourses.
    The attribute "total" is added to the object, storing the
    sum of all credits for courses in the QuerySet.
    The attribute "earned" is added to the object, storing the
    sum of all credits for all completed coruses in the QuerySet.
    """
    qs = EDCourse.objects.filter(student=user).order_by(
        'course__subject',
        'course__number'
    )
    qs = calculate_credits(qs)

    return qs


def WSPcourses(user):
    """
    Returns a QuerySet object of all of the user's EDCourses with subject WSP.
    The attribute "total" is added to the object, storing the
    sum of all credits for courses in the QuerySet.
    """
    qs = EDCourse.objects.filter(
        student=user,
        course__subject__short='WSP'
    ).order_by('course__number')
    qs = calculate_credits(qs)

    return qs


def courses_by_division(user):
    """
    Returns a dictionary.
    Keys are the names of each Division object.
    Values are QuerySet objects of the user's EDCourses which belong to that
    divison.
    The attribute "total" is added to each QuerySet object, storing the
    sum of all credits for courses in the associated division.
    """
    divcourses = {}
    divisions = Division.objects.values_list('name', flat=True)

    for div in divisions:
        qs = EDCourse.objects.filter(
                student=user,
                course__subject__department__division__name=div
             ).order_by('course__subject', 'course__number')
        qs = calculate_credits(qs)
        divcourses[div] = qs

    return divcourses


def major_courses(user, major):
    """

    """
    qs = EDCourse.objects.filter(student=user).order_by(
        'course__subject',
        'course__number',
    )
    # firgures out which major it's getting information for
    if major == 1:
        qs = qs.filter(maj1=True)
    elif major == 2:
        qs = qs.filter(maj2=True)

    # calculates the number of credits this major has
    if qs:
        qs = calculate_credits(qs)
    # gets the name and description of the major
    try:
        the_major = Major.objects.get(student=user, number=major)
    except Major.DoesNotExist:
        return None
    qs.title = the_major.title
    qs.description = the_major.description
    # returns all the information
    return qs


def minor_courses(user, minor):
    """

    """
    qs = EDCourse.objects.filter(student=user).order_by(
        'course__subject',
        'course__number',
    )
    # firgures out which minor it's getting information for
    if minor == 1:
        qs = qs.filter(min1=True)
    elif minor == 2:
        qs = qs.filter(min2=True)
    # calculates the number of credits this minor has
    if qs:
        qs = calculate_credits(qs)
    # gets the name and description of the minor
    try:
        the_minor = Minor.objects.get(student=user, number=minor)
    except Minor.DoesNotExist:
        return None
    qs.title = the_minor.title
    qs.description = the_minor.description
    # returns all the information
    return qs


def supporting_courses(user):
    """
    returns a query set of all classes that aren't in a major
    or are a WSP class
    """
    # excludes all the classes that are already part of a major or minor
    qs = EDCourse.objects.filter(student=user).order_by(
        'course__subject',
        'course__number',
    )
    qs = qs.exclude(maj1=True)\
           .exclude(maj2=True)\
           .exclude(min1=True)\
           .exclude(min2=True)\
           .exclude(course__subject__short='WSP')
    # calculates the number of credits this major has
    if qs:
        qs = calculate_credits(qs)

    return qs


def approved_courses(user):
    """
    returns a query set of approved courses
    """
    qs = ApprovedCourse.objects.filter(student=user).order_by(
        'course__subject',
        'course__number',
    )
    qs = calculate_credits(qs)

    return qs

def semester_courses(user):
    """
    returns a dictionary of courses broken up by term

    """
    qs = EDCourse.objects.filter(student=user).order_by(
        'term__code'
    )
    
    terms_dict = { course.term : [] for course in qs }

    for course in qs:
        terms_dict[course.term].append(course)

    #assert False 
    return terms_dict
