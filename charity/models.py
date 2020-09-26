import datetime

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MinValueValidator, RegexValidator, MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


zip_code_regex = RegexValidator(
    regex=r'\d{2}-\d{3}',
    message='Proszę wprowadzić kod pocztowy w odpowiednim formacie: 00-000',
)
phone_regex = RegexValidator(
    regex=r'^\+?1?\d{8,15}$',
    message='Proszę podać numer komórkowy lub stacjonarny poprzedzony numerem kierunkowym, bez spacji (223334455)',
)
min_bag_quantity = MinValueValidator(
    limit_value=1,
    message='Ilość oddanych worków musi być większa od 0',
)
min_working_hours = MinValueValidator(
    limit_value=datetime.time(hour=8, minute=00, second=00),
    message='Odbiór można zlecić w godzinach 8:00 - 20:00',
)
max_working_hours = MaxValueValidator(
    limit_value=datetime.time(hour=20, minute=00, second=00),
    message='Odbiór można zlecić w godzinach 8:00 - 20:00',
)


def one_day_hence():
    return timezone.now().date() + timezone.timedelta(days=1)


tomorrow_date = MinValueValidator(
    limit_value=one_day_hence,
    message='Data odbioru nie może być z przeszłości',
)


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name=_('name'))

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Kategoria'
        verbose_name_plural = 'Kategorie'


class Institution(models.Model):
    FOUNDATION = 'FUN'
    NGO = 'NGO'
    LOCAL_COLLECTION = 'LOC'
    TYPE_OF_INSTITUTION = [
        (FOUNDATION, 'Fundacja'),
        (NGO, 'Organizacja pozarządowa'),
        (LOCAL_COLLECTION, 'Lokalna zbiórka'),
    ]
    name = models.CharField(max_length=64,
                            unique=True,
                            verbose_name=_('name'))
    description = models.CharField(max_length=256,
                                   verbose_name=_('description'))
    type = models.CharField(max_length=3,
                            choices=TYPE_OF_INSTITUTION,
                            default=FOUNDATION,
                            verbose_name=_('type'))
    categories = models.ManyToManyField(Category, verbose_name=_('categories'))

    def __str__(self):
        return f'{self.name}\n' \
               f'{self.description}'

    class Meta:
        verbose_name = 'Instytucja'
        verbose_name_plural = 'Instytucje'


class Donation(models.Model):
    BOOL_CHOICES = (
        (False, _('No')),
        (True, _('Yes')),
    )

    quantity = models.IntegerField(validators=[min_bag_quantity],
                                   verbose_name=_('quantity'), )
    street = models.CharField(max_length=256,
                              verbose_name=_('street'), )
    city = models.CharField(max_length=64,
                            verbose_name=_('city'), )
    zip_code = models.CharField(max_length=6,
                                validators=[zip_code_regex],
                                verbose_name=_('zip code'), )
    phone_number = models.CharField(max_length=15,
                                    validators=[phone_regex],
                                    verbose_name=_('phone number'), )
    pick_up_date = models.DateField(validators=[tomorrow_date],
                                    verbose_name=_('pick up date'), )
    pick_up_time = models.TimeField(validators=[min_working_hours, max_working_hours],
                                    verbose_name=_('pick up time'), )
    pick_up_comment = models.CharField(max_length=256,
                                       blank=True,
                                       default='',
                                       verbose_name=_('comment'), )
    is_taken = models.BooleanField(choices=BOOL_CHOICES,
                                   default=False,
                                   verbose_name=_("picked up"), )
    is_taken_date = models.DateField(blank=True,
                                     null=True,
                                     verbose_name=_('pick up confirmation date'), )
    institution = models.ForeignKey(Institution,
                                    on_delete=models.CASCADE,
                                    verbose_name=_('institution'), )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             null=True,
                             default=None,
                             verbose_name=_('user'))
    categories = models.ManyToManyField(Category, verbose_name=_('categories'))

    def __init__(self, *args, **kwargs):
        super(Donation, self).__init__(*args, **kwargs)
        self.old_is_taken = self.is_taken

    def save(self, *args, **kwargs):
        """ On save where is_taken changed to True, update timestamp of is_taken_date """
        if self.old_is_taken is False and self.is_taken is True:
            self.is_taken_date = timezone.now()
        return super(Donation, self).save(*args, **kwargs)

    def __str__(self):
        return f'Przekazanie {self.quantity} worków/a {self.categories.__str__()} organizacji - \n' \
               f'{self.institution.__str__()}'

    @property
    def is_taken_str(self):
        return _("Yes") if self.is_taken else _("No")

    class Meta:
        verbose_name = 'Dotacja'
        verbose_name_plural = 'Dotacje'
        ordering = ['is_taken', '-pick_up_date', ]
