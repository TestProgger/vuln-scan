from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth import hashers
from project.users.consts import UserRole as UserRoleEnum
from uuid import uuid4


class UserManager(BaseUserManager):
    def _create_user(self, password, **extra_fields):
        user = self.model(**extra_fields)
        user.password = hashers.make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(password, **extra_fields)

    def create_superuser(self, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        role = UserRole.objects.get(code=UserRoleEnum.ADMINISTRATOR.value)
        extra_fields.setdefault("role_id", role.id)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(password, **extra_fields)


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid4
    )

    middle_name = models.CharField(
        max_length=150, blank=True, verbose_name="Отчество"
    )

    role = models.ForeignKey(
        "users.UserRole", on_delete=models.RESTRICT, verbose_name="Роль"
    )

    email = None

    objects = UserManager()

    EMAIL_FIELD = None
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

    class Meta:
        db_table = "user"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователь"


class UserRole(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid4
    )

    name = models.CharField(
        max_length=150, unique=True
    )

    code = models.CharField(
        max_length=150, unique=True, db_index=True
    )

    priority = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "user_role"