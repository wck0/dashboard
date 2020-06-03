from django.contrib import admin
from vita.models import *

# None Text Filters

class GradSemFilter(admin.SimpleListFilter):
    title = 'Graduation Semester'
    parameter_name = 'grad_sem'

    def lookups(self, request, model_admin):
        return (
            (1, 'January'),
            (2, 'Spring'),
            (6, 'Summer'),
            (9, 'Fall'),
        )
    
    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(grad_term__code__endswith=self.value())

# Parent text filter 

class InputFilter(admin.SimpleListFilter):
    template = 'vita/input_filter.html'

    def lookups(self, request, model_admin):
        # Dummy, required to show the filter.
        return ((),)

    def choices(self, changelist):
        # Grab only the "all" option.
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice


# Child text filters

class GradYearFilter(InputFilter):
    title = 'Graduation Year'
    parameter_name = 'grad_year'

    def queryset(self, request, queryset):
        if self.value() is not None:
            year = self.value()
            
            return queryset.filter(grad_term__code__startswith=year)

class AdvisorFilter(InputFilter):
    title = 'Advisor Last Name'
    parameter_name = 'advisor_name'

    def queryset(self, request, queryset):
        if self.value() is not None:
            advisor_name = self.value()

            return queryset.filter(advisor_email__icontains=advisor_name[0:7])

class SponsorFilter(InputFilter):
    title = 'Sponsor Last Name'
    parameter_name = 'sponsor_name'

    def queryset(self, request, queryset):
        if self.value() is not None:
            sponsor_name = self.value()

            return queryset.filter(sponsor_email__icontains=sponsor_name[0:7])
