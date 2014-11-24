from django import forms
from web_ide.models import Developer
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserChangeForm, UserCreationForm


class CustomDeveloperCreationForm(forms.ModelForm):
    username = forms.CharField(label='Username')
    email = forms.CharField(label='Email address')
    pw1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    pw2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    is_superuser = forms.BooleanField(label='Is Administrator?', required=False)

    class Meta(UserCreationForm.Meta):
        model = Developer
        fields = ('username', 'email')

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            Developer.objects.get(username=username)
        except Developer.DoesNotExist:
            return username

        raise forms.ValidationError(_("Duplicate username"), code='invalid name')


    def clean_pw2(self):
        pw1 = self.cleaned_data.get("pw1")
        pw2 = self.cleaned_data.get("pw2")

        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError(_("Passwords must match."), code="pw mismatch")

        if len(pw1) < 6:
            raise forms.ValidationError(_("Password too short"), code="pw too short")

        return pw2

    def save(self, commit=True):
        user = super(CustomDeveloperCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["pw2"])
        if commit:
            user.save()
        return user


class CustomDeveloperChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label="password",
                                         help_text="""You can't view/change the password""")
    is_superuser = forms.BooleanField(label='Is Administrator?', required=False)
    is_active = forms.BooleanField(label='Is active?', required=False)

    class Meta(UserChangeForm.Meta):
        model = Developer
        fields = ('username', 'email', 'password', 'is_active', 'is_superuser')

    def clean_password(self):
        return self.initial["password"]