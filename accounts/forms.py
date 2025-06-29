from django import forms
from .models import userProfile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = userProfile
        fields = ['profile_picture', 'bio', 'github', 'twitter']