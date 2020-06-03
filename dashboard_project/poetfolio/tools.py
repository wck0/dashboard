from django.contrib.auth.models import User, Group

# some common tools, useful across the site

# user/group checks
def is_student(user):
    return user.groups.filter(name='Student').exists()

def is_council(user):
    return user.groups.filter(name='Council').exists()

def is_WSPstaff(user):
    return user.groups.filter(name='WSP Staff').exists()

def all_students():
    return User.objects.filter(groups__name='Student').order_by('last_name')
