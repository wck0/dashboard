from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(HeroImage)
class HeroImageAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return []

@admin.register(RequiredCourses)
class EDCourseAdmin(admin.ModelAdmin):
    fields = ( 'course', 'credits')
    list_display = ('course',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return []
