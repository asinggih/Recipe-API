from django.db import models
from django.contrib.auth.models import \
    AbstractBaseUser, \
    BaseUserManager, \
    PermissionsMixin

from django.conf import settings


class UserManager(BaseUserManager):

    # **extra_fields makes it easier when adding more arguments later on
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves new user"""

        # if email is empty raise a valueError
        if not email:
            raise ValueError('Users must have an email address')
        # Normalising the email using a helper function from BaseUserManager
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # need set_password() so that password is encrypted
        user.set_password(password)
        # this is to support multiple databases (best practice)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""

        # This is only for django admin purposes
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instad of username"""

    # Defining fields of our db model below

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # create a UserManager Object
    objects = UserManager()

    # override default username to use email
    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """Tag to be used for a recipe"""

    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,   # which model we're depending on
        on_delete=models.CASCADE,   # delete tag when owner is deleted
    )

    def __str__(self):
        return self.name
