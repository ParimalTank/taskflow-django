from django import forms
from django.contrib.auth.models import User
from .models import Organization, Invitation, Membership


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Acme Corp'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'What is this organization about? (optional)'}),
        }


class InviteForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username to invite'}),
    )
    role = forms.ChoiceField(
        choices=[('MEMBER', 'Member'), ('ADMIN', 'Admin')],
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    def __init__(self, *args, organization=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.organization = organization

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError(f'No user found with username "{username}".')

        if self.organization:
            if Membership.objects.filter(user=user, organization=self.organization).exists():
                raise forms.ValidationError(f'"{username}" is already a member of this organization.')
            if Invitation.objects.filter(invited_user=user, organization=self.organization, status='PENDING').exists():
                raise forms.ValidationError(f'"{username}" already has a pending invitation.')

        return username
