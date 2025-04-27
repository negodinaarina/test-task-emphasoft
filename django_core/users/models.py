from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from users.constants import NAME_MAX_LENGTH
from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        CUSTOMER = "CUSTOMER"
        ADMIN = "ADMIN"

    last_name = models.CharField(
        verbose_name="Last name", max_length=NAME_MAX_LENGTH, blank=True
    )
    first_name = models.CharField(
        verbose_name="First name", max_length=NAME_MAX_LENGTH, blank=True
    )
    middle_name = models.CharField(
        verbose_name="Middle name", max_length=NAME_MAX_LENGTH, null=True, blank=True
    )
    email = models.EmailField(
        verbose_name="email address",
        unique=True,
        error_messages={
            "unique": "User with given email already exists",
        },
    )
    role = models.CharField(
        verbose_name="Role", choices=Role.choices, default=Role.CUSTOMER
    )
    date_joined = models.DateTimeField(
        verbose_name="Registration date", default=timezone.now
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_staff(self):
        return self.role == self.Role.ADMIN

    @property
    def is_superuser(self):
        return self.role == self.Role.ADMIN
