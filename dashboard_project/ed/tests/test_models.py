from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from ed.models import *

# TODO: class CourseModelTest(TestCase):
# TODO: class EDCourseModelTest(TestCase):
# TODO: class ApprovedCourseModelTest(TestCase):
# TODO: class EducationalGoalModelTest(TestCase):
# TODO: relocate EDCourseForm to forms.py; update all references accordingly

class TermModelTest(TestCase):
    def test_saving_and_retrieving_terms(self):
        term = Term()
        term.code = 201901
        term.save()
        
        other_term = Term()
        other_term.code = 202002
        other_term.save()
        
        saved_terms = Term.objects.all()
        self.assertEqual(saved_terms.count(), 2)
        
        first_saved_term = saved_terms[0]
        second_saved_term = saved_terms[1]
        
        self.assertEqual(first_saved_term, term)
        self.assertEqual(first_saved_term.code, 201901)
        self.assertEqual(first_saved_term.year(), 2019)
        self.assertEqual(first_saved_term.month(), 1)
        self.assertEqual(first_saved_term.name(), 'January')
        
        self.assertEqual(second_saved_term, other_term)
        self.assertEqual(second_saved_term.code, 202002)
        self.assertEqual(second_saved_term.year(), 2020)
        self.assertEqual(second_saved_term.month(), 2)
        self.assertEqual(second_saved_term.name(), 'Spring')
    
    def test_cannot_save_empty_term(self):
        term = Term()
        with self.assertRaises(IntegrityError):
            term.save()
            term.full_clean()

class DivisionModelTest(TestCase):
    def test_saving_and_retrieving_divisions(self):
        division = Division()
        division.code = 1
        division.name = "Humanities"
        division.save()
        
        other_division = Division()
        other_division.code = 2
        other_division.name = "Natural Sciences"
        other_division.save()
        
        saved_divisions = Division.objects.all()
        self.assertEqual(saved_divisions.count(), 2)
        
        first_saved_division = saved_divisions[0]
        second_saved_division = saved_divisions[1]
        
        self.assertEqual(first_saved_division, division)
        self.assertEqual(first_saved_division.code, 1)
        self.assertEqual(first_saved_division.name, "Humanities")
        
        self.assertEqual(second_saved_division, other_division)
        self.assertEqual(second_saved_division.code, 2)
        self.assertEqual(second_saved_division.name, "Natural Sciences")
    
    def test_cannot_save_empty_division(self):
        division = Division()
        with self.assertRaises(IntegrityError):
            division.save()
            division.full_clean()
    
class DepartmentModelTest(TestCase):
    def test_saving_and_retrieving_department(self):
        division = Division()
        division.code = 1
        division.name = "Humanities"
        division.save()
        
        department = Department()
        department.name = "English"
        department.division = division
        department.save()
        
        saved_departments = Department.objects.all()
        self.assertEqual(saved_departments.count(), 1)
        
        first_saved_department = saved_departments[0]
        self.assertEqual(first_saved_department.name, "English")
        self.assertEqual(first_saved_department.division, division)
    
    def test_cannot_save_empty_department(self):
        department = Department()
        with self.assertRaises(IntegrityError):
            department.save()
            department.full_clean()
            
class SubjectModelTest(TestCase):
    def test_saving_and_retrieving_subject(self):
        division = Division()
        division.code = 2
        division.name = "Natural Sciences"
        division.save()
        
        department = Department()
        department.name = "Mathematics & Computer Science"
        department.division = division
        department.save()
        
        other_department = Department()
        other_department.name = "Biology"
        other_department.division = division
        other_department.save()
        
        subject = Subject()
        subject.name = "Mathematics"
        subject.short = "MATH"
        subject.department = department
        subject.save()
        
        other_subject = Subject()
        other_subject.name = "Biology"
        other_subject.short = "BIOL"
        other_subject.department = other_department
        other_subject.save()
        
        saved_subjects = Subject.objects.all()
        self.assertEqual(saved_subjects.count(), 2)
        
        first_saved_subject = saved_subjects[0]
        second_saved_subject = saved_subjects[1]
        
        self.assertEqual(first_saved_subject.name, "Mathematics")
        self.assertEqual(first_saved_subject.short, "MATH")
        self.assertEqual(first_saved_subject.department, department)
        self.assertEqual(first_saved_subject.department.division, division)
        self.assertEqual(second_saved_subject.name, "Biology")
        self.assertEqual(second_saved_subject.short, "BIOL")
        self.assertEqual(second_saved_subject.department, other_department)
        self.assertEqual(second_saved_subject.department.division, division)
    
    def test_cannot_save_empty_subject(self):
        subject = Subject()
        with self.assertRaises(ValidationError):
            subject.save()
            subject.full_clean()
    
    def test_can_save_subject_without_department(self):
        subject = Subject()
        subject.name = "Mathematics"
        subject.short = "MATH"
        subject.save()
        
        first_saved_subject = Subject.objects.first()
        self.assertEqual(first_saved_subject, subject)
        self.assertIsNone(first_saved_subject.department)

class MajorMinorModelTest(TestCase):
    def test_can_save_and_retrieve_major_and_minor(self):
        student = User()
        student.username = "a student"
        student.set_password("secure password")
        student.save()
        other_student = User()
        other_student.username = "another student"
        other_student.set_password("secure password")
        other_student.save()
        
        major = Major()
        major.student = student
        major.title = "Sport on Film"
        major.description = "A study of how sport is shown on the big screen"
        major.number = 1
        major.save()
        
        other_major = Major()
        other_major.student = other_student
        other_major.title = "Film Marketing"
        other_major.description = "Tricking people into watching movies"
        other_major.number = 1
        other_major.save()
        
        saved_majors = Major.objects.all()
        self.assertEqual(saved_majors.count(), 2)
        
        first_saved_major = saved_majors[0]
        second_saved_major = saved_majors[1]
        
        self.assertEqual(first_saved_major, major)
        self.assertEqual(first_saved_major.student, student)
        self.assertEqual(first_saved_major.title, "Sport on Film")
        self.assertEqual(first_saved_major.description,
                         "A study of how sport is shown on the big screen")
        self.assertEqual(first_saved_major.number, 1)
        self.assertEqual(second_saved_major, other_major)
        self.assertEqual(second_saved_major.student, other_student)
        self.assertEqual(second_saved_major.title, "Film Marketing")
        self.assertEqual(second_saved_major.description,
                         "Tricking people into watching movies")
        self.assertEqual(second_saved_major.number, 1)

        minor = Minor()
        minor.student = student
        minor.title = "Sport on Film"
        minor.description = "A study of how sport is shown on the big screen"
        minor.number = 1
        minor.save()
        
        other_minor = Minor()
        other_minor.student = other_student
        other_minor.title = "Film Marketing"
        other_minor.description = "Tricking people into watching movies"
        other_minor.number = 1
        other_minor.save()
        
        saved_minors = Minor.objects.all()
        self.assertEqual(saved_minors.count(), 2)
        
        first_saved_minor = saved_minors[0]
        second_saved_minor = saved_minors[1]
        
        self.assertEqual(first_saved_minor, minor)
        self.assertEqual(first_saved_minor.student, student)
        self.assertEqual(first_saved_minor.title, "Sport on Film")
        self.assertEqual(first_saved_minor.description,
                         "A study of how sport is shown on the big screen")
        self.assertEqual(first_saved_minor.number, 1)
        self.assertEqual(second_saved_minor, other_minor)
        self.assertEqual(second_saved_minor.student, other_student)
        self.assertEqual(second_saved_minor.title, "Film Marketing")
        self.assertEqual(second_saved_minor.description,
                         "Tricking people into watching movies")
        self.assertEqual(second_saved_minor.number, 1)
