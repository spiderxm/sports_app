from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, age, sport, state, password, **extra_fields):
        """
        Create and save a User with the given email, password and given details
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, sport=sport, state=state, age=age ** extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, age, sport, state, password, **extra_fields):
        """
        Create and save a SuperUser with the given email, password and details.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, age, sport, state, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    age = models.PositiveIntegerField(blank=False, default=0)
    sport = models.ForeignKey()
    state = models.CharField(blank=False, max_length=256, default="none")
    is_staff = models.BooleanField(default=False)
    highest_qualification = models.CharField(default="none")
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Sport(models.Model):
    """
    Sport model will store various sports played.
    """
    sport = models.CharField()


class State(models.Model):
    """
    State model stores various states in india
    """
    state = models.CharField()

    def __str__(self):
        return self.state


class UnionTerritory(models.Model):
    """
    UnionTerritory models store various union territory in india
    """
    UnionTerritory = models.CharField()

    def __str__(self):
        return self.UnionTerritory