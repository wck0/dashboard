from django import forms
from .models import EducationalGoal, EDCourse
from django.contrib.admin.widgets import FilteredSelectMultiple

class EducationalGoalForm(forms.ModelForm):

    courses = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        
    )
    
    class Meta:
        model = EducationalGoal
        fields = ('title', 'description', 'courses')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(EducationalGoalForm, self).__init__(*args, **kwargs)
        qs = EDCourse.objects.filter(student=user)
        for edcourse in qs:
            self.fields['courses'].choices = [(edcourse.id, str(edcourse))
                                        for edcourse in qs] 

class ApprovedCourseForm(forms.ModelForm):
    
    approved = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        
    )
    
    class Meta:
        model = EDCourse
        fields = ('approved',)
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ApprovedCourseForm, self).__init__(*args, **kwargs)
        qs = EDCourse.objects.filter(student=user)
        for edcourse in qs:
            self.fields['approved'].choices = [(edcourse.id,)
                                        for edcourse in qs]
