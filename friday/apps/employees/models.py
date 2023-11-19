from django.db import models
from django.utils import timezone


class Employee(models.Model):
    user = models.OneToOneField('accounts.User', related_name='employee',
                                on_delete=models.CASCADE)
    code = models.CharField(max_length=255)

    class Role(models.IntegerChoices):
        PRODUCT_MANAGER = 1
        TESTER = 2
        DEVELOPER = 3
    role = models.PositiveSmallIntegerField(choices=Role.choices)
    created = models.DateTimeField(default=timezone.localtime)

    def __str__(self) -> str:
        return self.code
