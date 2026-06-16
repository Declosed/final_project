from django import forms
from django.contrib.auth.models import User
from .models import StudentProfile

class PortalRegistrationForm(forms.ModelForm):
    # Map explicit frontend label variables
    username = forms.CharField(label="Username Handle", max_length=150)
    email = forms.EmailField(label="Email Address")
    password = forms.CharField(label="Password Secret", widget=forms.PasswordInput)
    
    program_track = forms.ChoiceField(
        label="Choose Program Track",
        choices=StudentProfile.TRACK_CHOICES,
        widget=forms.Select()
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A student with this email address already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"]) # Hashes the password safely
        if commit:
            user.save()
            # Provision profile matching track choice selection
            StudentProfile.objects.create(
                user=user, 
                program_track=self.cleaned_data.get('program_track')
            )
        return user
