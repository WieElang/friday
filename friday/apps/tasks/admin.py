from django.contrib import admin
from django.http.request import HttpRequest

from friday.apps.employees.models import Employee
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'issue',)

    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return request.user.is_superuser or request.user.employee.role == Employee.Role.DEVELOPER


admin.site.register(Task, TaskAdmin)
