from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.db.models import Max
from django.contrib.auth.models import User, Group
from django.urls import reverse
from poetfolio.views import *
from vita.models import Menu_item, Home_page
from ed.tools import *
from siteconfig.models import HeroImage

class IndexTest(TestCase):
    def setUp(self):
        home = Home_page.objects.create(image=None,
                                        text='hello!',
                                       )
        menu = Menu_item.objects.create(title='a thing',
                                        subtitle='stuff about the thing',
                                        link = '/',
                                        thumbnail=None,
                                        order = '1'
                                       )
        student_group = Group.objects.create(name='Student')
        test_student = User.objects.create_user(username='test_student',
                                                password='thisisastudent',
                                               )
        test_student.groups.add(student_group)
        
        council_group = Group.objects.create(name='Council')
        test_council = User.objects.create_user(username='test_council',
                                                password='thisiscouncil',
                                               )
        
        test_council.groups.add(council_group)
        
        wspstaff_group = Group.objects.create(name='WSP Staff')
        test_wspstaff = User.objects.create_user(username='test_wspstaff',
                                                password='thisiswspstaff',
                                               )
        test_wspstaff.groups.add(wspstaff_group)
    
    def test_anonymous_user_can_view(self):
        response = self.client.get(reverse(Index))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
    
    def test_student_can_view(self):
        test_student = User.objects.get(username='test_student')
        logged_in = self.client.force_login(test_student)
        
        response = self.client.get(reverse(Index))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        
    
    def test_council_can_view(self):
        test_council = User.objects.get(username='test_council')
        logged_in = self.client.force_login(test_council)
        
        response = self.client.get(reverse(Index))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
    
    def test_wspstaff_can_view(self):
        test_wspstaff = User.objects.get(username='test_wspstaff')
        logged_in = self.client.force_login(test_wspstaff)
        
        response = self.client.get(reverse(Index))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
