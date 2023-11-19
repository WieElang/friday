from django.contrib import admin
from django.http.request import HttpRequest
from .models import Employee


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('code', 'role',)

    def has_module_permission(self, request: HttpRequest) -> bool:
        return request.user.is_superuser


admin.site.register(Employee, EmployeeAdmin)
