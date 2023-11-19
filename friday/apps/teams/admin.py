from django.contrib import admin
from django.http.request import HttpRequest
from .models import Teams


class TeamsAdmin(admin.ModelAdmin):
    list_display = ('name',)

    def has_module_permission(self, request: HttpRequest) -> bool:
        return request.user.is_superuser


admin.site.register(Teams, TeamsAdmin)
