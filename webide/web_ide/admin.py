from django.contrib import admin
from django.contrib.admin import AdminSite
from web_ide.models import Developer
from web_ide.forms import CustomDeveloperChangeForm, CustomDeveloperCreationForm


class DeveloperAdmin(admin.ModelAdmin):
    change_form = CustomDeveloperChangeForm
    add_form = CustomDeveloperCreationForm

    list_display = ('username', 'email', 'is_superuser')
    list_filter = ('is_superuser',)

    change_fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_superuser', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'pw1', 'pw2', 'is_superuser')}
         ),
    )

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            return self.add_form
        else:
            return self.change_form

    search_fields = ('email', 'username')
    ordering = ('email',)


class AdministratorSite(AdminSite):
    site_header = "WebIDE Administration"
    site_title = "WebIDE"
    index_title = "WebIDE Administration"

# Register your models here.
admin_site = AdministratorSite(name='myadmin')
admin_site.register(Developer, DeveloperAdmin)