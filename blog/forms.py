from django import forms
from .models import blogsite_post , comments

class blog_form(forms.ModelForm):
    class Meta:
        model= blogsite_post

        fields= ['title','content']  # Specify the fields to include in the form

class comment_form(forms.ModelForm):
    class Meta:
        model = comments
        fields = ['content'] 