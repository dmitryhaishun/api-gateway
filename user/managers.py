from datetime import date
from typing import Optional

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class MyUserManager(BaseUserManager):
    def get_by_natural_key(self, username: str) -> Optional[AbstractBaseUser]:
        return self.get(**{self.model.USERNAME_FIELD: username})

    def create_user(self, email: str, password: str, first_name: str, last_name: str) -> AbstractBaseUser:
        """
        Create and save a new user with the given email and password.
        """
        if not email:
            raise ValueError("The Email field must be set")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            birth_date=date(1990, 5, 24),
            is_staff=True,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, first_name: str, last_name: str) -> AbstractBaseUser:
        """
        Create and save a new superuser with the given email and password.
        """
        user = self.create_user(email, password=password, first_name=first_name, last_name=last_name)
        user.is_admin = True
        user.save(using=self._db)
        return user
