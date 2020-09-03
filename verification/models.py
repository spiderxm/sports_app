from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import MinLengthValidator


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, first_name, last_name, gender, age, sport, state, password, **extra_fields):
        """
        Create and save a User with the given email, password and given details
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, gender=gender, sport=sport,
                          state=state, age=age,
                          **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, gender, age, sport, state, password, **extra_fields):
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
        return self.create_user(email, first_name, last_name, gender, age, sport, state, password, **extra_fields)


Gender = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Rather not say', 'Rather not say')
]


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model - for registering user
    """
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=256, default=None,
                                  validators=[MinLengthValidator(2, "Minimum length should be greater than 2")])
    last_name = models.CharField(max_length=256, default=None,
                                 validators=[MinLengthValidator(2, "Minimum length should be greater than 2")])
    gender = models.CharField(max_length=256, choices=Gender, default='Male')
    age = models.PositiveIntegerField(blank=False, default=18)
    sport = models.ForeignKey(to='Sport', default='Cricket', on_delete=models.PROTECT)
    state = models.ForeignKey(to='State', default='Assam', on_delete=models.PROTECT)
    highest_qualification = models.CharField(default="none", max_length=256)
    is_staff = models.BooleanField(default=False)
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
    sport = models.CharField(max_length=256,
                             null=True,
                             validators=[MinLengthValidator(2, "minimum length should be greater than 2")])

    def __str__(self):
        return self.sport

    class Meta:
        db_table = "sport"


class State(models.Model):
    """
    State model stores various states in india
    """
    state = models.CharField(max_length=256,
                             default="None",
                             null=True,
                             validators=[MinLengthValidator(2, "minimum length should be greater than 2")])

    def __str__(self):
        return self.state

    class Meta:
        db_table = "state"


class UnionTerritory(models.Model):
    """
    UnionTerritory models store various union territory in india
    """
    Union_territory = models.CharField(max_length=256,
                                       null=True,
                                       validators=[MinLengthValidator(2, "minimum length should be greater than 2")])

    def __str__(self):
        return self.Union_territory

    class Meta:
        db_table = "unionterritories"


class ProfilePicture(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to='profile_pics')

    def __str__(self):
        return '{} Profile Picture'.format(self.user.email)


# Create your models here.
class user_achievements(models.Model):
    '''
    Model to store details of users
    '''
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    Name_of_Tournament = models.CharField(max_length=256, default="", null=False)
    date = models.DateField(null=False)
    Venue = models.CharField(max_length=256, null=False)
    Event = models.CharField(max_length=256, null=False)
    Medal_won = models.CharField(max_length=256, null=False)

    def __str__(self):
        return self.user.email + ''' ''' +self.Event
