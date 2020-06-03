from ed.models import EDCourse, ApprovedCourse

for course in EDCourse.objects.all():
    if ApprovedCourse.objects.filter(student=course.student, course=course.course).exists():
        approved = ApprovedCourse.objects.get(student=course.student, course=course.course)
        approved.edcourseID = course.id
        approved.save()

