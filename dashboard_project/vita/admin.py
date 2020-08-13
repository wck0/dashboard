from django.contrib import admin

from vita.models import *
from vita.filters import *
# Register your models here.


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
            'user', 
            'student_id', 
            'grad_term', 
            'advisor_email', 
            'sponsor_email', 
            'ED_meeting_complete', 
            'PR_meeting_complete', 
            'active'
            )
    
    search_fields = [
            'user__username', 
            'user__first_name', 
            'user__last_name',
            'student_id'
            ]
    
    list_filter = (
            GradYearFilter,
            GradSemFilter,
            AdvisorFilter,
            SponsorFilter,
            'ED_meeting_complete', 
            'PR_meeting_complete', 
            'active',
            )
    list_per_page = 50

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    search_fields = ['user__username',
                     'user__first_name', 'user__last_name',
                     'essay',
                    ]
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

@admin.register(OffCampusExperience)
class OffCampusExperienceAdmin(admin.ModelAdmin):
    search_fields = ['user__username',
                     'user__first_name', 'user__last_name',
                     'essay',
                    ]
    
    list_display = (
            'user',
            'experince_type',
            'approved',
            'completed',
            )

    list_filter = (
            'experince_type',
            'approved',
            'completed',
            )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

@admin.register(Menu_item)
class MenuIitemAdmin(admin.ModelAdmin):
    list_display = ('title','order')
    ordering = ('order',)
    
@admin.register(Home_page)
class HomePage(admin.ModelAdmin):
    list_display = ('publish_date',)
    ordering = ('publish_date',)
