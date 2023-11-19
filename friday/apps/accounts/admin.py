from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _

from .models import User


class UserAdminForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"../password/\">this form</a>."))

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(DjangoUserAdmin):
    form = UserAdminForm
    fieldsets = (
        (None, {'fields': ('name', 'email', 'password',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}),
    )
    list_display = ('name', 'email', 'is_staff', 'is_active',)
    search_fields = ('name', 'email',)
    ordering = ('name',)

    def has_module_permission(self, request: HttpRequest) -> bool:
        return request.user.is_superuser


admin.site.register(User, UserAdmin)
