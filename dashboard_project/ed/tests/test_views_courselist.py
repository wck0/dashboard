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
from datetime import date

# TODO: class AddCourseTest(TestCase):
# TODO: class DeleteEDCourseTest(TestCase):


class CourseListTest(TestCase):
    def setUp(self):
        student_group = Group.objects.create(name='Student')
        test_student = User.objects.create_user(
            username='test_student',
            password='thisisastudent',
        )
        test_student.groups.add(student_group)

        subject = Subject()
        subject.name = "English"
        subject.short = "ENGL"
        subject.save()

        other_subject = Subject()
        other_subject.name = "Biology"
        other_subject.short = "BIOL"
        other_subject.save()

        course = Course()
        course.subject = subject
        course.number = "120"
        course.title = "Why Read?"
        course.save()

        other_course = Course()
        other_course.subject = other_subject
        other_course.number = "151"
        other_course.title = "Cell & Molecular Biology"
        other_course.save()

        edcourse = EDCourse()
        edcourse.student = test_student
        edcourse.course = course
        edcourse.credits = 3
        edcourse.save()

        other_edcourse = EDCourse()
        other_edcourse.student = test_student
        other_edcourse.course = other_course
        other_edcourse.credits = 4
        other_edcourse.save()

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

    def test_login_required(self):
        response = self.client.get(reverse(CourseList))
        redirect_path = reverse('login') + '?next=' + reverse(CourseList)
        self.assertRedirects(response, redirect_path)

    def test_student_post_request(self):
        test_student = User.objects.get(username='test_student')
        logged_in = self.client.force_login(test_student)
        response = self.client.post(reverse(CourseList))
        redirect_path = reverse('Index')
        # assertRedirects doesn't work right after POST?
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, redirect_path)

    def test_student_get_request(self):
        test_student = User.objects.get(username='test_student')
        logged_in = self.client.force_login(test_student)
        response = self.client.get(reverse(CourseList))

        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'], test_student)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertTemplateUsed(response, 'ed/courselist.html')

        self.assertIn('pagename', response.context)
        self.assertEqual('Course List', response.context['pagename'])

        self.assertIn('usercourses', response.context)
        usercourses = all_courses(test_student)
        # https://stackoverflow.com/a/49129560/1205608
        self.assertQuerysetEqual(
            usercourses,
            response.context['usercourses'],
            transform=lambda x: x
        )

        try:
            hero = HeroImage.objects.get(app='ed')
        except HeroImage.DoesNotExist:
            hero = None
        self.assertIn('hero', response.context)
        self.assertEqual(hero, response.context['hero'])

    def test_council_post_request_student_exists(self):
        test_council = User.objects.get(username='test_council')
        test_student = User.objects.get(username='test_student')
        logged_in = self.client.force_login(test_council)
        response = self.client.post(
            reverse(CourseList),
            {'student': test_student.id},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            reverse(CourseList)+test_student.username
        )

    def test_council_post_request_student_does_not_exist(self):
        test_council = User.objects.get(username='test_council')
        test_student = User.objects.get(username='test_student')
        logged_in = self.client.force_login(test_council)

        max_id = User.objects.all().aggregate(Max('id'))['id__max']

        response = self.client.post(
            reverse(CourseList),
            {'student': max_id+1},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse(CourseList))

    def test_council_get_request_picker(self):
        test_council = User.objects.get(username='test_council')
        logged_in = self.client.force_login(test_council)
        response = self.client.get(reverse(CourseList))

        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'], test_council)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertTemplateUsed(response, 'ed/studentpickerform.html')

        self.assertIn('pagename', response.context)
        self.assertEqual('Select Student', response.context['pagename'])

        studentlist = all_students()
        self.assertIn('students', response.context)
        self.assertQuerysetEqual(
            studentlist,
            response.context['students'],
            transform=lambda x: x,
        )

        try:
            hero = HeroImage.objects.get(app='ed')
        except HeroImage.DoesNotExist:
            hero = None

        self.assertIn('hero', response.context)
        self.assertEqual(hero, response.context['hero'])

    def test_wspstaff_post_request_student_exists(self):
        test_wspstaff = User.objects.get(username='test_wspstaff')
        test_student = User.objects.get(username='test_student')
        logged_in = self.client.force_login(test_wspstaff)
        response = self.client.post(
            reverse(CourseList),
            {'student': test_student.id},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            reverse(CourseList) + test_student.username,
        )

    def test_wspstaff_post_request_student_does_not_exist(self):
        test_wspstaff = User.objects.get(username='test_wspstaff')
        test_student = User.objects.get(username='test_student')
        logged_in = self.client.force_login(test_wspstaff)

        max_id = User.objects.all().aggregate(Max('id'))['id__max']

        response = self.client.post(
            reverse(CourseList),
            {'student': max_id+1},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse(CourseList))

    def test_wspstaff_get_request_picker(self):
        test_wspstaff = User.objects.get(username='test_wspstaff')
        logged_in = self.client.force_login(test_wspstaff)
        response = self.client.get(reverse(CourseList))

        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'], test_wspstaff)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertTemplateUsed(response, 'ed/studentpickerform.html')

        self.assertIn('pagename', response.context)
        self.assertEqual('Select Student', response.context['pagename'])

        studentlist = all_students()
        self.assertIn('students', response.context)
        self.assertQuerysetEqual(
            studentlist,
            response.context['students'],
            transform=lambda x: x,
        )

        try:
            hero = HeroImage.objects.get(app='ed')
        except HeroImage.DoesNotExist:
            hero = None

        self.assertIn('hero', response.context)
        self.assertEqual(hero, response.context['hero'])


class EditEDCourseTest(TestCase):
    def setUp(self):
        student_group = Group.objects.create(name='Student')
        test_student = User.objects.create_user(
            username='test_student',
            password='thisisastudent',
        )
        test_student.groups.add(student_group)

        other_test_student = User.objects.create_user(
            username='other_student',
            password='anotherstudent',
        )
        other_test_student.groups.add(student_group)

        term = Term()
        term.code = "202009"
        term.save()

        subject = Subject()
        subject.name = "English"
        subject.short = "ENGL"
        subject.save()

        other_subject = Subject()
        other_subject.name = "Biology"
        other_subject.short = "BIOL"
        other_subject.save()

        course = Course()
        course.subject = subject
        course.number = "120"
        course.title = "Why Read?"
        course.save()

        other_course = Course()
        other_course.subject = other_subject
        other_course.number = "151"
        other_course.title = "Cell & Molecular Biology"
        other_course.save()

        edcourse = EDCourse()
        edcourse.student = test_student
        edcourse.course = course
        edcourse.credits = 3
        edcourse.save()

        other_edcourse = EDCourse()
        other_edcourse.student = test_student
        other_edcourse.course = other_course
        other_edcourse.credits = 4
        other_edcourse.save()

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

    def test_anonymous_user_redirected_to_login(self):
        response = self.client.get(reverse(EditEDCourse))
        redirect_path = reverse('login') + '?next=' + reverse(EditEDCourse)
        self.assertRedirects(response, redirect_path)

        response = self.client.post(
            reverse('editEDCourse'),
            {'edcourse_id': 0},
        )
        self.assertRedirects(response, redirect_path)

    def test_council_redirected_to_index(self):
        test_council = User.objects.get(username='test_council')
        logged_in = self.client.force_login(test_council)

        redirect_path = reverse('Index')
        response = self.client.get(reverse('editEDCourse'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, redirect_path)

        response = self.client.post(
            reverse(EditEDCourse),
            {'edcourse_id': 0},
        )
        # assertRedirects doesn't work right after POST?
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, redirect_path)

    def test_wspstaff_redirected_to_index(self):
        test_wspstaff = User.objects.get(username='test_wspstaff')
        logged_in = self.client.force_login(test_wspstaff)

        redirect_path = reverse('Index')
        response = self.client.get(reverse('editEDCourse'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, redirect_path)

        response = self.client.post(
            reverse(EditEDCourse),
            {'edcourse_id': 0},
        )
        # assertRedirects doesn't work right after POST?
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, redirect_path)

    def test_student_can_edit_own_edcourse(self):
        test_student = User.objects.get(username='test_student')
        logged_in = self.client.force_login(test_student)

        edcourse = EDCourse.objects.filter(student=test_student).first()

        engl = Subject.objects.get(short="ENGL")
        self.assertEqual(edcourse.course.subject, engl)

        biol = Subject.objects.get(short="BIOL")
        cellbio = Course.objects.get(
            subject=biol,
            number="151",
            title="Cell & Molecular Biology",
        )

        payload = {
            'subject': biol.short or '',
            'number': cellbio.number or '',
            'title': cellbio.title or '',
            'term': '09',
            'year': '2020',
            'cr': edcourse.credits or '',
            'crn': edcourse.crn or '',
            'instructor': 'Kronholm' or '',
            'completed': int(edcourse.completed) or 0,
            'maj1': int(edcourse.maj1) or 0,
            'maj2': int(edcourse.maj2) or 0,
            'min1': int(edcourse.min1) or 0,
            'min2': int(edcourse.min2) or 0,
            'is_whittier': int(edcourse.is_whittier) or 0,
            'notes': edcourse.notes or '',
        }
        response = self.client.post(
            reverse('editEDCourse') + str(edcourse.id),
            payload,
        )
        self.assertRedirects(response, reverse('CourseList'))

        new_edcourse = EDCourse.objects.filter(student=test_student).first()
        self.assertEqual(new_edcourse.course, cellbio)
        self.assertEqual(new_edcourse.term.code, 202009),
        self.assertEqual(new_edcourse.instructor, 'Kronholm')

    def test_student_cannot_edit_others_edcourse(self):
        test_student = User.objects.get(username='test_student')
        other_student = User.objects.get(username='other_student')
        logged_in = self.client.force_login(other_student)

        edcourse = EDCourse.objects.filter(student=test_student).first()

        engl = Subject.objects.get(short="ENGL")
        self.assertEqual(edcourse.course.subject, engl)
        whyread = Course.objects.get(
            subject=engl,
            number="120",
            title="Why Read?",
        )

        biol = Subject.objects.get(short="BIOL")
        cellbio = Course.objects.get(
            subject=biol,
            number="151",
            title="Cell & Molecular Biology",
        )

        payload = {
            'subject': biol.short or '',
            'number': cellbio.number or '',
            'title': cellbio.title or '',
            'term': '09',
            'year': '2020',
            'cr': edcourse.credits or '',
            'crn': edcourse.crn or '',
            'instructor': 'Kronholm' or '',
            'completed': int(edcourse.completed) or 0,
            'maj1': int(edcourse.maj1) or 0,
            'maj2': int(edcourse.maj2) or 0,
            'min1': int(edcourse.min1) or 0,
            'min2': int(edcourse.min2) or 0,
            'is_whittier': int(edcourse.is_whittier) or 0,
            'notes': edcourse.notes or '',
        }
        response = self.client.post(
            reverse('editEDCourse') + str(edcourse.id),
            payload,
        )
        # assertRedirects doesn't work right after POST?
        redirect_path = reverse('Index')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, redirect_path)

        new_edcourse = EDCourse.objects.filter(student=test_student).first()
        self.assertEqual(new_edcourse.course, whyread)
        self.assertEqual(new_edcourse.term, None),
        self.assertEqual(new_edcourse.instructor, None)


class AddCourseTest(TestCase):
    def setUp(self):
        student_group = Group.objects.create(name='Student')
        test_student = User.objects.create_user(
            username='test_student',
            password='thisisastudent',
        )
        test_student.groups.add(student_group)

        other_test_student = User.objects.create_user(
            username='other_student',
            password='anotherstudent',
        )
        other_test_student.groups.add(student_group)

        term = Term()
        term.code = 202009
        term.save()

        subject = Subject()
        subject.name = "English"
        subject.short = "ENGL"
        subject.save()

        other_subject = Subject()
        other_subject.name = "Biology"
        other_subject.short = "BIOL"
        other_subject.save()

        course = Course()
        course.subject = subject
        course.number = "120"
        course.title = "Why Read?"
        course.save()

        other_course = Course()
        other_course.subject = other_subject
        other_course.number = "151"
        other_course.title = "Cell & Molecular Biology"
        other_course.save()

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

    def test_council_redirects(self):
        redirect_path = reverse('Index')

        test_council = User.objects.get(username="test_council")
        self.assertTrue(is_council(test_council))

        logged_in = self.client.force_login(test_council)

        response = self.client.get(reverse('AddCourse'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, redirect_path)

        response = self.client.post(reverse('AddCourse'), {})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, redirect_path)

    def test_cwspstaff_redirects(self):
        redirect_path = reverse('Index')

        test_wspstaff = User.objects.get(username="test_wspstaff")
        self.assertTrue(is_WSPstaff(test_wspstaff))

        logged_in = self.client.force_login(test_wspstaff)

        response = self.client.get(reverse('AddCourse'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, redirect_path)

        response = self.client.post(reverse('AddCourse'), {})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, redirect_path)

    def test_student_get_request(self):
        test_student = User.objects.get(username="test_student")
        self.assertTrue(is_student(test_student))

        logged_in = self.client.force_login(test_student)

        response = self.client.get(reverse('AddCourse'))
        year = date.today().year
        years = [i for i in range(year-4, year+4)]
        subjects = Subject.objects.all()
        subjs = [s.short for s in subjects]

        test_student_courses = all_courses(test_student)

        try:
            hero = HeroImage.objects.get(app='ed')
        except HeroImage.DoesNotExist:
            hero = None

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ed/AddEDCourse.html')
        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'], test_student)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertIn('years', response.context)
        self.assertEqual(response.context['years'], years)
        self.assertIn('subjects', response.context)
        self.assertEqual(response.context['subjects'], sorted(subjs))
        self.assertIn('hero', response.context)
        self.assertEqual(response.context['hero'], hero)
        self.assertIn('usercourses', response.context)
        self.assertQuerysetEqual(
            test_student_courses,
            response.context['usercourses'],
            transform=lambda x: x,
        )

    def test_student_can_add_one_course(self):
        test_student = User.objects.get(username="test_student")
        self.assertTrue(is_student(test_student))

        logged_in = self.client.force_login(test_student)

        engl = Subject.objects.get(short="ENGL")
        whyread = Course.objects.get(
            subject=engl,
            number="120",
            title="Why Read?",
        )

        payload = {
            'subject': engl.short,
            'number': whyread.number,
            'title': whyread.title,
            'term': '09',
            'year': '2020',
            'credits': '3',
            'crn': '',
            'instructor': '',
            'completed': '1',
            'maj1': '1',
            'maj2': '0',
            'min1': '0',
            'min2': '1',
            'is_whittier': '1',
            'notes': 'I really want to know why I should read.',
        }

        response = self.client.post(reverse('AddCourse'), payload)

        redirect_path = reverse('AddCourse')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, redirect_path)

        edcourse = EDCourse.objects.filter(student=test_student)[0]
        term = Term.objects.get(code=202009)
        self.assertEqual(edcourse.course, whyread)
        self.assertEqual(edcourse.term, term)
        self.assertEqual(edcourse.credits, 3)
        self.assertTrue(edcourse.completed)
        self.assertTrue(edcourse.maj1)
        self.assertFalse(edcourse.maj2)
        self.assertFalse(edcourse.min1)
        self.assertTrue(edcourse.min2)
        self.assertTrue(edcourse.is_whittier)
        self.assertEqual(
            edcourse.notes,
            'I really want to know why I should read.'
        )

    def test_student_can_add_many_courses(self):
        test_student = User.objects.get(username="test_student")
        self.assertTrue(is_student(test_student))

        logged_in = self.client.force_login(test_student)

        engl = Subject.objects.get(short="ENGL")
        whyread = Course.objects.get(
            subject=engl,
            number="120",
            title="Why Read?",
        )

        biol = Subject.objects.get(short="BIOL")
        cellbio = Course.objects.get(
            subject=biol,
            number="151",
            title="Cell & Molecular Biology",
        )

        payload = {
            'subject': [engl.short, biol.short],
            'number': [whyread.number, cellbio.number],
            'title': [whyread.title, cellbio.title],
            'term': ['09', '09'],
            'year': ['2020', '2020'],
            'credits': ['3', '3'],
            'crn': ['', ''],
            'instructor': ['', ''],
            'completed': ['1', '0'],
            'maj1': ['1', '0'],
            'maj2': ['0', '1'],
            'min1': ['0', '1'],
            'min2': ['1', '0'],
            'is_whittier': ['1', '1'],
            'notes': [
                'I really want to know why I should read.',
                '',
            ],
        }

        response = self.client.post(reverse('AddCourse'), payload)

        redirect_path = reverse('AddCourse')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, redirect_path)

        edcourse = EDCourse.objects.filter(student=test_student)[0]
        term = Term.objects.get(code=202009)
        self.assertEqual(edcourse.course, whyread)
        self.assertEqual(edcourse.term, term)
        self.assertEqual(edcourse.credits, 3)
        self.assertTrue(edcourse.completed)
        self.assertTrue(edcourse.maj1)
        self.assertFalse(edcourse.maj2)
        self.assertFalse(edcourse.min1)
        self.assertTrue(edcourse.min2)
        self.assertTrue(edcourse.is_whittier)
        self.assertEqual(
            edcourse.notes,
            'I really want to know why I should read.'
        )

        edcourse = EDCourse.objects.filter(student=test_student)[1]
        term = Term.objects.get(code=202009)
        self.assertEqual(edcourse.course, cellbio)
        self.assertEqual(edcourse.term, term)
        self.assertEqual(edcourse.credits, 3)
        self.assertFalse(edcourse.completed)
        self.assertFalse(edcourse.maj1)
        self.assertTrue(edcourse.maj2)
        self.assertTrue(edcourse.min1)
        self.assertFalse(edcourse.min2)
        self.assertTrue(edcourse.is_whittier)
        self.assertEqual(
            edcourse.notes,
            ''
        )
