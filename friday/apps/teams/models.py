from django.db import models
from django.utils import timezone


class Teams(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    employees = models.ManyToManyField('employees.Employee', related_name='teams', blank=True)
    projects = models.ManyToManyField('projects.Project', related_name='teams')
    created = models.DateTimeField(default=timezone.localtime)

    def __str__(self) -> str:
        return self.name
