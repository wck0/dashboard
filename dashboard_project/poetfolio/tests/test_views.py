from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.db.models import Max
from django.contrib.auth.models import User, Group
from django.urls import reverse
from .views import *
from vita.models import Menu_item, Home_page
from ed.tools import *
from siteconfig.models import HeroImage

class IndexTest(TestCase):
    def SetUp(self):
        home = Home_page.objects.create(image=None,
                                        text=None,
                                       )
        
