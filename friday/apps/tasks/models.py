from django.db import models
from django.utils import timezone


class Task(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey('accounts.User', related_name='tasks',
                             on_delete=models.CASCADE)
    project = models.ForeignKey('projects.Project', related_name='tasks',
                                on_delete=models.CASCADE)
    issue = models.ForeignKey('issues.Issue', related_name='tasks',
                              on_delete=models.CASCADE)

    class Status(models.IntegerChoices):
        TODO = 1
        WIP = 2
        NEED_REVIEW = 3
        NEED_CHANGES = 4
        DONE = 5
        HOLD = 6
    status = models.PositiveSmallIntegerField(choices=Status.choices,
                                              default=Status.TODO)

    notes = models.TextField(blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)
    updated = models.DateField(default=timezone.localdate)
    created = models.DateTimeField(default=timezone.localtime)

    def __str__(self) -> str:
        return self.name


class TaskActivity(models.Model):
    task = models.ForeignKey(Task, related_name="activities",
                             on_delete=models.CASCADE)
    old_status = models.PositiveSmallIntegerField(choices=Task.Status.choices)
    new_status = models.PositiveSmallIntegerField(choices=Task.Status.choices)
    created = models.DateTimeField(default=timezone.localtime)

    def __str__(self) -> str:
        return self.task.name


class Comment(models.Model):
    user = models.ForeignKey('accounts.User', related_name='comments',
                             on_delete=models.CASCADE)
    task = models.ForeignKey(Task, related_name='comments',
                             on_delete=models.CASCADE)
    message = models.TextField()
    created = models.DateTimeField(default=timezone.localtime)

    def __str__(self) -> str:
        return self.message
