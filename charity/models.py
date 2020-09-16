from datetime import datetime

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy
from django.utils import timezone

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
    limit_value=datetime.time(8, 00, 00),
    message='Odbiór można zlecić w godzinach 8:00 - 20:00',
)
max_working_hours = MinValueValidator(
    limit_value=datetime.time(20, 00, 00),
    message='Odbiór można zlecić w godzinach 8:00 - 20:00',
)


def one_day_hence():
    return timezone.now() + timezone.timedelta(days=1)


tomorrow_date = MinValueValidator(
    limit_value=one_day_hence(),
    message='Data odbioru nie może być z przeszłości',
)


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name=gettext_lazy('name'))

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Kategoria'
    #     verbose_name_plural = 'Kategorie'


class Institution(models.Model):
    FOUNDATION = 'FUN'
    NGO = 'NGO'
    LOCAL_COLLECTION = 'LOC'
    TYPE_OF_INSTITUTION = [
        (FOUNDATION, 'Fundacja'),
        (NGO, 'Organizacja pozarządowa'),
        (LOCAL_COLLECTION, 'Lokalna zbiórka'),
    ]
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=256)
    type = models.CharField(max_length=3, choices=TYPE_OF_INSTITUTION, default=FOUNDATION)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return f'{self.name}\n' \
               f'{self.description}'

    class Meta:
        verbose_name = 'Instytucja'
    #     verbose_name_plural = 'Instytucje'


class Donation(models.Model):
    quantity = models.IntegerField(validators=[min_bag_quantity])
    street = models.CharField(max_length=256)
    city = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=6, validators=[zip_code_regex])
    # Could use PhoneNumberField instead
    phone_number = models.CharField(max_length=15, validators=[phone_regex])
    pick_up_date = models.DateField(validators=[tomorrow_date])
    pick_up_time = models.TimeField(validators=[min_working_hours, max_working_hours])
    pick_up_comment = models.CharField(max_length=256, blank=True, null=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return f'Przekazanie {self.quantity} worków {self.categories.__str__()} przekazanych\n' \
               f'{self.institution.__str__()}'

    class Meta:
        verbose_name = 'Dotacja'
    #     verbose_name_plural = 'Dotacje'
