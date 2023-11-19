from django.db import models
from django.utils import timezone


class Issue(models.Model):
    project = models.ForeignKey('projects.Project', related_name='issues',
                                on_delete=models.CASCADE)
    creator = models.ForeignKey('accounts.User', related_name='created_issues',
                                on_delete=models.CASCADE)
    assigned = models.ForeignKey('accounts.User', related_name='assigned_issues',
                                 on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)

    class Status(models.IntegerChoices):
        TODO = 1
        WIP = 2
        PENDING_REVIEW = 3
        NEED_DEPLOY = 4
        NEED_UPLOAD = 5
        TESTING = 6
        DONE = 7
        CLOSED = 8
        HOLD = 9
    status = models.PositiveSmallIntegerField(choices=Status.choices,
                                              default=Status.TODO)

    class Priority(models.IntegerChoices):
        LOW = 1
        MEDIUM = 2
        HIGH = 3
        HIGHEST = 4
    priority = models.PositiveSmallIntegerField(choices=Priority.choices)
    deadline_date = models.DateField(blank=True, null=True)
    created = models.DateTimeField(default=timezone.localtime)

    def __str__(self) -> str:
        return self.title


class IssueCheckList(models.Model):
    issue = models.ForeignKey(Issue, related_name='checklists',
                              on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_checked = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class IssueActivity(models.Model):
    issue = models.ForeignKey(Issue, related_name='activities',
                              on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', related_name='issue_activities',
                             on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    created = models.DateTimeField(default=timezone.localtime)

    def __str__(self) -> str:
        return self.issue.title
