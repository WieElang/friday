from django.contrib import admin
from django.http.request import HttpRequest
from .models import Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active',)
    search_fields = ('name',)
    ordering = ('priority',)

    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return request.user.is_superuser


admin.site.register(Project, ProjectAdmin)
