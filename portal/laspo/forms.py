from django import forms
from django.contrib.auth.models import User
from .models import StudentProfile, ProgramTrack

class PortalRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    program_track = forms.ChoiceField(choices=ProgramTrack.choices, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            StudentProfile.objects.create(
                user=user,
                program_track=self.cleaned_data['program_track']
            )
        return user
