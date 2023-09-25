import datetime
import re
from typing import Any, Optional

from django.contrib.auth.base_user import AbstractBaseUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import EmailField

from user.managers import MyUserManager
from user.utils import user_uuid


class User(AbstractBaseUser):
    uuid = models.UUIDField(
        unique=True,
        blank=False,
        default=user_uuid,
    )
    first_name = models.CharField(
        validators=[
            RegexValidator(regex=r"^[A-Za-zА-Яа-я\s\'-]{2,30}$", message="Invalid name.", code="invalid_username"),
        ],
        blank=False,
    )
    last_name = models.CharField(
        validators=[
            RegexValidator(regex=r"^[A-Za-zА-Яа-я\s\'-]{2,30}$", message="Invalid last name.", code="invalid_username"),
        ],
        blank=False,
    )
    passport_id = models.CharField(
        validators=[
            RegexValidator(
                regex=r"^[A-Z0-9]{6,20}$",
                message="Passport number must must contain uppercase english letters and contain between "
                "6 and 20 digits",
                code="invalid_passport_number",
            )
        ],
        unique=True,
        blank=False,
    )
    birth_date = models.DateField(blank=False)
    email = models.EmailField(
        max_length=55,
        unique=True,
        blank=False,
    )
    phone_number = models.CharField(
        validators=[
            RegexValidator(
                regex=re.compile(r"^\+\d{11,12}$"),
                message="Phone number must start with  +  and contain between 11 and 12 digits",
                code="invalid_phone",
            ),
        ],
        unique=True,
        blank=False,
    )
    password = models.CharField(
        validators=[
            RegexValidator(
                regex=re.compile(
                    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_\-+=<>?[\]{};:\/<>,.'\-_...])[A-Za-z\d!@#$%^&*()"
                    r"_\-+=<>?[\]{};:\/<>,.'\-_...]{6,20}$"
                ),
                message="Password must contain at least one uppercase letter, one lowercase letter, one digit,"
                " and one special character",
            )
        ],
        blank=False,
    )
    create_at = models.DateTimeField(default=datetime.datetime.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = MyUserManager()

    def __str__(self) -> EmailField:
        return self.email

    def has_perm(self, perm: str, obj: Optional[Any] = None) -> bool:
        """
        for creating superuser
        """
        # Handle permissions
        return True

    def has_module_perms(self, app_label: str) -> bool:
        """
        for creating superuser
        """
        return True

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["email"], name="unique_email"),
            models.UniqueConstraint(fields=["passport_id"], name="unique_passport_id"),
            models.UniqueConstraint(fields=["phone_number"], name="unique_phone_number"),
        ]
