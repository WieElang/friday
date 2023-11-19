from django.urls import path
from .views import IssueIndex, IssueDetail, EditStatusIssue, EditChecklist

app_name = "issues"

urlpatterns = [
    path('', IssueIndex.as_view(), name='index'),
    path('details', IssueDetail.as_view(), name='details'),
    path('edit-status', EditStatusIssue.as_view(), name='edit_status_issue'),
    path('edit-checklist', EditChecklist.as_view(), name='edit_checklist'),
]
