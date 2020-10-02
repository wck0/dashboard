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


class EDViewTest(TestCase):
    def setUp(self):
        student_group = Group.objects.create(name='Student')
        student = User()
        student.username = "a student"
        student.set_password("secure password")
        student.save()
        student.groups.add(student_group)

        humanities = Division()
        humanities.code = 1
        humanities.name = "Humanities"
        humanities.save()

        interdisciplinary = Division()
        interdisciplinary.code = 4
        interdisciplinary.name = "Interdisciplinary"
        interdisciplinary.save()

        english = Department()
        english.name = "English"
        english.division = humanities
        english.save()

        wsp = Department()
        wsp.name = "Whittier Scholars Program"
        wsp.division = interdisciplinary
        wsp.save()

        subjectENGL = Subject()
        subjectENGL.name = "English"
        subjectENGL.short = "ENGL"
        subjectENGL.department = english
        subjectENGL.save()

        subjectWSP = Subject()
        subjectWSP.name = "Whittier Scholars"
        subjectWSP.short = "WSP"
        subjectWSP.department = wsp
        subjectWSP.save()

        course = Course()
        course.subject = subjectENGL
        course.number = "120"
        course.title = "Why Read?"
        course.save()

        other_course = Course()
        other_course.subject = subjectENGL
        other_course.number = "203"
        other_course.title = "Writing Poetry"
        other_course.save()

        wsp_course = Course()
        wsp_course.subject = subjectWSP
        wsp_course.number = "101"
        wsp_course.title = "The Individual, Identity & Community"
        wsp_course.save()

        major1 = Major()
        major1.student = student
        major1.title = "Underbasket Waterweaving"
        major1.number = 1
        major1.save()

        minor1 = Minor()
        minor1.student = student
        minor1.title = "Weaving Under Basket Water"
        minor1.number = 1
        minor1.save()

        council_group = Group.objects.create(name='Council')
        test_council = User.objects.create_user(
            username='test_council',
            password='thisiscouncil',
        )

        test_council.groups.add(council_group)

        wspstaff_group = Group.objects.create(name='WSP Staff')
        test_wspstaff = User.objects.create_user(
            username='test_wspstaff',
            password='thisiswspstaff',
        )
        test_wspstaff.groups.add(wspstaff_group)

    def test_student_can_get_ED(self):
        student = User.objects.get(username="a student")
        logged_in = self.client.force_login(student)
        response = self.client.get(reverse('ED'))

        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'], student)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertTemplateUsed(response, 'ed/ED.html')

        self.assertIn('username', response.context)
        self.assertEqual(response.context['username'], student.username)

        self.assertIn('usercourses', response.context)
        # https://stackoverflow.com/a/49129560/1205608
        self.assertQuerysetEqual(
            all_courses(student),
            response.context['usercourses'],
            transform=lambda x: x
        )

        self.assertIn('divcourses', response.context)
        # https://stackoverflow.com/a/49129560/1205608
        self.assertQuerysetEqual(
            courses_by_division(student),
            response.context['divcourses'],
            transform=lambda x: x
        )


        self.assertIn('major1', response.context)
        # https://stackoverflow.com/a/49129560/1205608
        self.assertQuerysetEqual(
            major_courses(student, 1),
            response.context['major1'],
            transform=lambda x: x
        )

        self.assertIn('major2', response.context)
        # empty Querysets can be checked with assertEqual
        # but not with assertQuerysetEqual that includes a transform
        self.assertEqual(major_courses(student, 2), response.context['major2'])

        self.assertIn('minor1', response.context)
        # https://stackoverflow.com/a/49129560/1205608
        self.assertQuerysetEqual(
            minor_courses(student, 1),
            response.context['minor1'],
            transform=lambda x: x
        )

        self.assertIn('minor2', response.context)
        # empty Querysets can be checked with assertEqual
        # but not with assertQuerysetEqual that includes a transform
        self.assertEqual(minor_courses(student, 2), response.context['minor2'])

        self.assertIn('wspcourses', response.context)
        # https://stackoverflow.com/a/49129560/1205608
        self.assertQuerysetEqual(
            WSPcourses(student),
            response.context['wspcourses'],
            transform=lambda x: x
        )


        self.assertIn('support', response.context)
        self.assertQuerysetEqual(
            supporting_courses(student),
            response.context['support'],
            transform=lambda x: x
        )

        self.assertIn('edgoals', response.context)
        # https://stackoverflow.com/a/49129560/1205608
        self.assertQuerysetEqual(
            EducationalGoal.objects.filter(student=student),
            response.context['edgoals'],
            transform=lambda x: x
        )

        try:
            s = Student.objects.get(user=student)
            narrative = s.narrative
        except Student.DoesNotExist:
            narrative = ""
        self.assertIn('narrative', response.context)
        self.assertEqual(response.context['narrative'], narrative)

        self.assertIn('pagename', response.context)
        self.assertEqual(response.context['pagename'], 'Educational Design')

        try:
            hero = HeroImage.objects.get(app='ed')
        except HeroImage.DoesNotExist:
            hero = None
        self.assertIn('hero', response.context)
        self.assertEqual(response.context['hero'], hero)
