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
        home.save()
        menu = Menu_item.objects.create(title='a thing',
                                        subtitle='stuff about the thing',
                                        link = '/',
                                        thumbnail=None,
                                        order = '1'
                                       )
        menu.save()
    
    def test_anonymous_user_can_view(self):
        response = self.client.get(reverse(Index))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
