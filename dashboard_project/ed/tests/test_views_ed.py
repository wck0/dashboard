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
from django.http import JsonResponse

# TODO: class EDTest(TestCase):
# TODO: class ApproveEDTest(TestCase):


class EDIndexViewTest(TestCase):
    def setup(self):
        pass

    def test_uses_landingpage_template(self):
        response = self.client.get(reverse(EDIndex))

        self.assertTemplateUsed(response, 'ed/landingpage.html')


class APIViewTest(TestCase):
    def setUp(self):
        student = User()
        student.username = "a student"
        student.set_password("secure password")
        student.save()

        subject = Subject()
        subject.name = "English"
        subject.short = "ENGL"
        subject.save()

        course = Course()
        course.subject = subject
        course.number = "120"
        course.title = "Why Read?"
        course.save()

        other_course = Course()
        other_course.subject = subject
        other_course.number = "203"
        other_course.title = "Writing Poetry"
        other_course.save()

    def test_response_empty_json_if_no_subject(self):
        student = User.objects.get(username="a student")
        logged_in = self.client.force_login(student)

        url = reverse('API')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(type(response), JsonResponse)
        self.assertJSONEqual(response.content.decode("utf-8"), {})

    def test_response_correct_when_subject_given_exists(self):
        student = User.objects.get(username="a student")
        logged_in = self.client.force_login(student)

        url = reverse('API') + 'ENGL/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(type(response), JsonResponse)
        self.assertJSONEqual(
            response.content.decode("utf-8"),
            {'120': '120', '203': '203'},
        )

    def test_response_correct_when_subject_given_does_not_exist(self):
        student = User.objects.get(username="a student")
        logged_in = self.client.force_login(student)

        url = reverse('API') + 'ZXCV/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(type(response), JsonResponse)
        self.assertJSONEqual(
            response.content.decode("utf-8"),
            {},
        )

    def test_response_correct_when_subject_and_number_exist(self):
        student = User.objects.get(username="a student")
        logged_in = self.client.force_login(student)

        url = reverse('API') + 'ENGL/203/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(type(response), JsonResponse)
        self.assertJSONEqual(
            response.content.decode("utf-8"),
            {'Writing Poetry': '203'},
        )

    def test_response_correct_when_subject_exists_but_number_does_not(self):
        student = User.objects.get(username="a student")
        logged_in = self.client.force_login(student)

        url = reverse('API') + 'ENGL/999/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(type(response), JsonResponse)
        self.assertJSONEqual(
            response.content.decode("utf-8"),
            {},
        )
