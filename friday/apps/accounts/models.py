from typing import Any

from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.db import models


class CustomUserManager(UserManager):

    def create_user(self, email: str, password: str, **extra_fields: Any) -> 'User':
        """
        Creates and saves a User with the given email and mobile_number.
        """

        user = self.model(email=email, is_superuser=False, is_staff=False, is_active=True,
                          **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email: str, password: str, **extra_fields: Any) -> 'User':
        user = self.create_user(email=email, password=password, **extra_fields)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(verbose_name='email address', unique=True, max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(verbose_name='staff status', default=False)
    is_superuser = models.BooleanField(verbose_name='superuser status', default=False)
    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    class Meta:
        db_table = 'users_user'

    def __str__(self) -> str:
        return self.name
