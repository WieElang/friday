from django.db import models
from django.utils import timezone


class Project(models.Model):
    name = models.CharField(max_length=255)

    class Priority(models.IntegerChoices):
        LOW = 1
        MEDIUM = 2
        HIGH = 3
        HIGHEST = 4
    priority = models.PositiveSmallIntegerField(choices=Priority.choices)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.localtime)

    def __str__(self) -> str:
        return self.name
