from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.db.models import Max
from django.contrib.auth.models import User, Group
from django.urls import reverse
from ed.views import *
from ed.models import *
from ed.tools import *
from siteconfig.models import HeroImage

# TODO: class APITest(TestCase):
# TODO: class EDTest(TestCase):
# TODO: class ApproveEDTest(TestCase):

class EDIndexTest(TestCase):
    def test_uses_landingpage_template(self):
        response = self.client.get(reverse(EDIndex))
        
        self.assertTemplateUsed(response, 'ed/landingpage.html')

