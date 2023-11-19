from django.contrib import admin
from .models import Issue, IssueCheckList


class IssueAdmin(admin.ModelAdmin):
    list_display = ('project', 'creator', 'assigned',
                    'title', 'status', 'priority', 'deadline_date',)
    search_fields = ('title', 'project', 'creator', 'assigned',)
    ordering = ('priority', 'status',)


class IssueChecklistAdmin(admin.ModelAdmin):
    list_display = ('issue', 'name', 'is_checked')
    search_fields = ('issue__name', 'name',)


admin.site.register(Issue, IssueAdmin)
admin.site.register(IssueCheckList, IssueChecklistAdmin)
