from django import forms
from web_ide.models import Developer


class DeveloperForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Developer
        fields = ('username', 'email', 'password')
