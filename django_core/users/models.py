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
        verbose_name="Фамилия", max_length=NAME_MAX_LENGTH, blank=True
    )
    first_name = models.CharField(
        verbose_name="Имя", max_length=NAME_MAX_LENGTH, blank=True
    )
    middle_name = models.CharField(
        verbose_name="Отчество", max_length=NAME_MAX_LENGTH, null=True, blank=True
    )
    email = models.EmailField(
        verbose_name="Электронная почта",
        unique=True,
        error_messages={
            "unique": "Пользователь с таким адресом электронной почты уже существует.",
        },
    )
    role = models.CharField(verbose_name="Роль", choices=Role.choices, default=Role.CUSTOMER)
    date_joined = models.DateTimeField(
        verbose_name="Дата регистрации", default=timezone.now
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_staff(self):
        return self.role == self.Role.ADMIN
