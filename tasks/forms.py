from django import forms
from django.contrib.auth.models import User
from organizations.models import Membership
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'assigned_to']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, organization=None, **kwargs):
        super().__init__(*args, **kwargs)
        if organization:
            member_ids = Membership.objects.filter(organization=organization).values_list('user_id', flat=True)
            self.fields['assigned_to'].queryset = User.objects.filter(id__in=member_ids)
            self.fields['assigned_to'].label_from_instance = lambda obj: obj.username
        self.fields['assigned_to'].required = False
        self.fields['assigned_to'].empty_label = 'Unassigned'
