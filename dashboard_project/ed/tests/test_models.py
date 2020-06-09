from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from ed.models import *

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
        other_student.set_password("more secure password")
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

class CourseModelTest(TestCase):
    def test_saving_and_retrieving_course(self):
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
        
        saved_courses = Course.objects.all()
        self.assertEqual(saved_courses.count(), 2)
        
        first_saved_course = saved_courses[0]
        second_saved_course = saved_courses[1]
        
        self.assertEqual(first_saved_course, course)
        self.assertEqual(first_saved_course.subject, subject)
        self.assertEqual(first_saved_course.number, "120")
        self.assertEqual(first_saved_course.title, "Why Read?")
        self.assertEqual(second_saved_course, other_course)
        self.assertEqual(second_saved_course.subject, other_subject)
        self.assertEqual(second_saved_course.number, "151")
        self.assertEqual(second_saved_course.title, "Cell & Molecular Biology")
        
    def test_cannot_save_empty_course(self):
        course = Course()
        with self.assertRaises(IntegrityError):
            course.save()
            course.full_clean()
    
    def test_cannot_save_course_without_subject(self):
        course = Course()
        course.number = "141"
        course.title = "Calculus & Analytical Geometry I"
        with self.assertRaises(IntegrityError):
            course.save()
            course.full_clean()
    
class EDCourseModelTest(TestCase):
    def test_saving_and_retrieving_edcourse(self):
        student = User()
        student.username = "a student"
        student.set_password("secure password")
        student.save()
        
        other_student = User()
        other_student.username = "another student"
        other_student.set_password("more secure password")
        other_student.save()
        
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
        edcourse.student = student
        edcourse.course = course
        edcourse.credits = 3
        edcourse.save()
        
        other_edcourse = EDCourse()
        other_edcourse.student = other_student
        other_edcourse.course = other_course
        other_edcourse.credits = 4
        other_edcourse.save()
        
        saved_edcourses = EDCourse.objects.all()
        self.assertEqual(saved_edcourses.count(), 2)
        
        first_saved_edcourse = saved_edcourses[0]
        second_saved_edcourse = saved_edcourses[1]
        
        self.assertEqual(first_saved_edcourse, edcourse)
        self.assertEqual(first_saved_edcourse.student, student)
        self.assertEqual(first_saved_edcourse.course, course)
        self.assertEqual(first_saved_edcourse.credits, 3)
        self.assertEqual(second_saved_edcourse, other_edcourse)
        self.assertEqual(second_saved_edcourse.student, other_student)
        self.assertEqual(second_saved_edcourse.course, other_course)
        self.assertEqual(second_saved_edcourse.credits, 4)
        
    def test_cannot_save_empty_edcourse(self):
        edcourse = EDCourse()
        with self.assertRaises(IntegrityError):
            edcourse.save()
            edcourse.full_clean()
    
    def test_cannot_save_edcourse_missing_student(self):
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
        
        # missing student
        edcourse = EDCourse()
        edcourse.course = course
        edcourse.credits = 3
        
        with self.assertRaises(IntegrityError):
            edcourse.save()
            edcourse.full_clean()
    
    def test_cannot_save_edcourse_missing_course(self):
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
        
        # missing course
        edcourse = EDCourse()
        edcourse.student = student
        edcourse.credits = 3
        
        with self.assertRaises(IntegrityError):
            edcourse.save()
            edcourse.full_clean()

    def test_cannot_save_edcourse_missing_credits(self):
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
        
        # missing credits
        edcourse = EDCourse()
        edcourse.student = student
        edcourse.course = course
        
        with self.assertRaises(IntegrityError):
            edcourse.save()
            edcourse.full_clean()

class ApprovedCourseModelTest(TestCase):
    def test_saving_and_retreiving_approvedcourse(self):
        student = User()
        student.name = "a student"
        student.set_password("secure password")
        student.save()
        
        other_student = User()
        other_student.username = "another student"
        other_student.set_password("more secure password")
        other_student.save()
        
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
        edcourse.student = student
        edcourse.course = course
        edcourse.credits = 3
        edcourse.save()
        
        other_edcourse = EDCourse()
        other_edcourse.student = other_student
        other_edcourse.course = other_course
        other_edcourse.credits = 4
        other_edcourse.save()
        
        approvedcourse = ApprovedCourse()
        approvedcourse.student = student
        approvedcourse.course = course
        approvedcourse.term = edcourse.term
        approvedcourse.credits = edcourse.credits
        approvedcourse.completed = edcourse.completed
        approvedcourse.crn = edcourse.crn
        approvedcourse.instructor = edcourse.instructor
        approvedcourse.maj1 = edcourse.maj1
        approvedcourse.maj2 = edcourse.maj2
        approvedcourse.min1 = edcourse.min1
        approvedcourse.min2 = edcourse.min2
        approvedcourse.is_whittier = edcourse.is_whittier
        approvedcourse.notes = edcourse.notes    
        approvedcourse.edcourseID = edcourse.id
        approvedcourse.save()
        
        other_approvedcourse = ApprovedCourse()
        other_approvedcourse.student = other_student
        other_approvedcourse.course = other_course
        other_approvedcourse.term = other_edcourse.term
        other_approvedcourse.credits = other_edcourse.credits
        other_approvedcourse.completed = other_edcourse.completed
        other_approvedcourse.crn = other_edcourse.crn
        other_approvedcourse.instructor = other_edcourse.instructor
        other_approvedcourse.maj1 = other_edcourse.maj1
        other_approvedcourse.maj2 = other_edcourse.maj2
        other_approvedcourse.min1 = other_edcourse.min1
        other_approvedcourse.min2 = other_edcourse.min2
        other_approvedcourse.is_whittier = other_edcourse.is_whittier
        other_approvedcourse.notes = other_edcourse.notes    
        other_approvedcourse.edcourseID = other_edcourse.id
        other_approvedcourse.save()
        
        all_approvedcourses = ApprovedCourse.objects.all()
        self.assertEqual(all_approvedcourses.count(), 2)
        
        first_saved_approvedcourse = all_approvedcourses[0]
        second_saved_approvedcourse = all_approvedcourses[1]
        
        self.assertEqual(first_saved_approvedcourse, approvedcourse)
        self.assertEqual(second_saved_approvedcourse, other_approvedcourse)
    
    def test_approvedcourse_student_is_edcourse_student(self):
        student = User()
        student.name = "a student"
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
        
        edcourse = EDCourse()
        edcourse.student = student
        edcourse.course = course
        edcourse.credits = 3
        edcourse.save()
        
        approvedcourse = ApprovedCourse()
        approvedcourse.student = student
        approvedcourse.course = course
        approvedcourse.term = edcourse.term
        approvedcourse.credits = edcourse.credits
        approvedcourse.completed = edcourse.completed
        approvedcourse.crn = edcourse.crn
        approvedcourse.instructor = edcourse.instructor
        approvedcourse.maj1 = edcourse.maj1
        approvedcourse.maj2 = edcourse.maj2
        approvedcourse.min1 = edcourse.min1
        approvedcourse.min2 = edcourse.min2
        approvedcourse.is_whittier = edcourse.is_whittier
        approvedcourse.notes = edcourse.notes    
        approvedcourse.edcourseID = edcourse.id
        approvedcourse.save()
        
        saved_approvedcourse = ApprovedCourse.objects.first()
        self.assertEqual(saved_approvedcourse, approvedcourse)
        
        the_edcourse = EDCourse.objects.get(id=saved_approvedcourse.edcourseID)
        self.assertEqual(the_edcourse.student, student)
        
    def test_cannot_save_approved_course_missing_student(self):
        student = User()
        student.name = "a student"
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
        
        edcourse = EDCourse()
        edcourse.student = student
        edcourse.course = course
        edcourse.credits = 3
        edcourse.save()
        
        approvedcourse = ApprovedCourse()
        #approvedcourse.student = student # missing student
        approvedcourse.course = course
        approvedcourse.term = edcourse.term
        approvedcourse.credits = edcourse.credits
        approvedcourse.completed = edcourse.completed
        approvedcourse.crn = edcourse.crn
        approvedcourse.instructor = edcourse.instructor
        approvedcourse.maj1 = edcourse.maj1
        approvedcourse.maj2 = edcourse.maj2
        approvedcourse.min1 = edcourse.min1
        approvedcourse.min2 = edcourse.min2
        approvedcourse.is_whittier = edcourse.is_whittier
        approvedcourse.notes = edcourse.notes    
        approvedcourse.edcourseID = edcourse.id
        
        with self.assertRaises(IntegrityError):
            approvedcourse.save()
            approvedcourse.full_clean()

    def test_cannot_save_approved_course_missing_course(self):
        student = User()
        student.name = "a student"
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
        
        edcourse = EDCourse()
        edcourse.student = student
        edcourse.course = course
        edcourse.credits = 3
        edcourse.save()
        
        approvedcourse = ApprovedCourse()
        approvedcourse.student = student
        #approvedcourse.course = course # missing course
        approvedcourse.term = edcourse.term
        approvedcourse.credits = edcourse.credits
        approvedcourse.completed = edcourse.completed
        approvedcourse.crn = edcourse.crn
        approvedcourse.instructor = edcourse.instructor
        approvedcourse.maj1 = edcourse.maj1
        approvedcourse.maj2 = edcourse.maj2
        approvedcourse.min1 = edcourse.min1
        approvedcourse.min2 = edcourse.min2
        approvedcourse.is_whittier = edcourse.is_whittier
        approvedcourse.notes = edcourse.notes    
        approvedcourse.edcourseID = edcourse.id
        
        with self.assertRaises(IntegrityError):
            approvedcourse.save()
            approvedcourse.full_clean()

    def test_cannot_save_approved_course_missing_credits(self):
        student = User()
        student.name = "a student"
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
        
        edcourse = EDCourse()
        edcourse.student = student
        edcourse.course = course
        edcourse.credits = 3
        edcourse.save()
        
        approvedcourse = ApprovedCourse()
        approvedcourse.student = student
        approvedcourse.course = course
        approvedcourse.term = edcourse.term
        #approvedcourse.credits = edcourse.credits # missing credits
        approvedcourse.completed = edcourse.completed
        approvedcourse.crn = edcourse.crn
        approvedcourse.instructor = edcourse.instructor
        approvedcourse.maj1 = edcourse.maj1
        approvedcourse.maj2 = edcourse.maj2
        approvedcourse.min1 = edcourse.min1
        approvedcourse.min2 = edcourse.min2
        approvedcourse.is_whittier = edcourse.is_whittier
        approvedcourse.notes = edcourse.notes    
        approvedcourse.edcourseID = edcourse.id
        
        with self.assertRaises(IntegrityError):
            approvedcourse.save()
            approvedcourse.full_clean()
