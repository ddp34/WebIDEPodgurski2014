from django import forms
from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserChangeForm, UserCreationForm
from django.contrib.auth.admin import UserAdmin
from web_ide.models import Developer


class CustomDeveloperCreationForm(UserCreationForm):
    pw1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    pw2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        model = Developer
        fields = ('username', 'email')

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            Developer._default_manager.get(username=username)
        except Developer.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def check_match(self):
        pw1 = self.cleaned_data.get("pw1")
        pw2 = self.cleaned_data.get("pw2")

        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError("Passwords must match.")
        return pw2

    def save(self, commit=True):
        developer = super(CustomDeveloperCreationForm, self).save(commit=False)
        developer.set_password(self.cleaned_data["pw1"])
        if commit:
            developer.save()
        return developer


class CustomDeveloperChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(label="password",
                                        help_text="""You can't actually view the password""")

    class Meta(UserChangeForm.Meta):
        model = Developer
        fields = ('username', 'email', 'password', 'is_active', 'is_superuser', 'user_permissions')

    def clean_password(self):
        return self.initial["password"]


class DeveloperAdmin(UserAdmin):
    form = CustomDeveloperChangeForm
    add_form = CustomDeveloperCreationForm

    list_display = ('username', 'email', 'is_superuser')
    list_filter = ('is_superuser',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'pw1', 'pw2', 'is_superuser')}
        ),
    )

    search_fields = ('email', 'username')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


# Register your models here.
admin.site.register(Developer, DeveloperAdmin)
