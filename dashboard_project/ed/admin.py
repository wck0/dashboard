from django.contrib import admin

# Register your models here.
from .models import *


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ('code',)
    search_fields = ['code']

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['code']
        else:
            return []

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return []


@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['name']
        else:
            return []

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return []


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'division')
    search_fields = ['name']

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['name']
        else:
            return []

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return []


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'short', 'department')
    search_fields = ['name', 'short']

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['name', 'short']
        else:
            return []

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return []


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('subject', 'number', 'title')
    search_fields = ['subject__name', 'subject__short', 'number', 'title']

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['subject']
        else:
            return []

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return []


@admin.register(Major, Minor)
class MajorMinorAdmin(admin.ModelAdmin):
    fields = ('student', 'title')
    list_display = ('student', 'title',)
    search_fields = [
        'student__username',
        'student__first_name',
        'student__last_name',
        'title',
    ]

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['student']
        else:
            return []

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return []


@admin.register(EDCourse)
class EDCourseAdmin(admin.ModelAdmin):
    fields = ('student', 'course', 'term', 'credits')
    list_display = ('student', 'course', 'term')
    search_fields = [
        'student__username',
        'student__first_name',
        'student__last_name',
        'course__title',
        'course__number',
        'course__subject__name',
        'course__subject__short',
    ]

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['student']
        else:
            return []

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return []


@admin.register(ApprovedCourse)
class ApprovedCourseAdmin(admin.ModelAdmin):
    fields = ('student', 'course', 'term', 'replacement',)
    list_display = ('student', 'course', 'term', 'replacement',)
    search_fields = [
        'student__username',
        'student__first_name',
        'student__last_name',
        'course__title',
        'course__number',
        'course__subject__name',
        'course__subject__short',
    ]

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['student']
        else:
            return []

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return []


@admin.register(EducationalGoal)
class EducationalGoalAdmin(admin.ModelAdmin):
    fields = ('student', 'title', 'description', 'courses')
    list_display = ('student', 'title', 'description', )
    search_fields = [
        'student__username',
        'student__first_name',
        'student__last_name',
        'title',
        'description',
    ]

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['student']
        else:
            return []

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return []
