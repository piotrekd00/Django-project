from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import Count
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils import timezone
from polymorphic.models import PolymorphicModel

from .validators import validate_digit_length, month
# Create your models here.


class RentalOffice(models.Model):
    name = models.CharField(max_length=32)
    address = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Item(PolymorphicModel):
    stock = models.IntegerField(default=0)


class Book(Item):
    author = models.CharField(max_length=16)
    title = models.CharField(max_length=32)
    genre = models.CharField(max_length=8)
    ISBN = models.CharField(max_length=13, unique=True, validators=[validate_digit_length])
    rentaloffice = models.ForeignKey(RentalOffice, on_delete=models.CASCADE)

    class Meta:
        unique_together = 'author', 'title', 'genre'

    def __str__(self):
        return self.title


class Film(Item):
    director = models.CharField(max_length=16)
    title = models.CharField(max_length=32)
    genre = models.CharField(max_length=8)
    duration = models.IntegerField(default=0)
    rentaloffice = models.ForeignKey(RentalOffice, on_delete=models.CASCADE)

    def validate_unique(self, exclude=None):
        if Film.objects.exclude(pk=self.pk).filter(director=self.director, title=self.title).exists():
            if Film.objects.filter(duration=self.duration):
                raise ValidationError('Duration must be different than other film with same title and director')
            super(Film, self).validate_unique(exclude=exclude)

    def clean(self):
        totals = Film.objects.values('genre').annotate(genre_count=Count('pk'))
        key_value = len(Film.objects.filter(genre=self.genre)) + 1
        print(Item.objects.all())
        for total in totals:
            min_val, max_val = total['genre_count'] - 3, total['genre_count'] + 3
            if key_value not in range(min_val, max_val+1):
                raise ValidationError('Difference from other genres must be in range of 3!')

    def __str__(self):
        return self.title


class CD(Item):
    band = models.CharField(max_length=16)
    genre = models.CharField(max_length=8)
    title = models.CharField(max_length=32)
    duration = models.IntegerField(default=0)
    rentaloffice = models.ForeignKey(RentalOffice, on_delete=models.CASCADE)
    songslist = ArrayField(
        ArrayField(
            models.CharField(max_length=10, blank=True),
            size=8,
        ),
        size=8
    )

    class Meta:
        unique_together = 'songslist', 'genre'

    def clean(self):
        totals = CD.objects.order_by().values('genre', 'band').distinct()
        max_genres_len = 0
        for total in totals:
            if total['band'] == self.band and not total['genre'] == self.genre:
                max_genres_len += 1
                if max_genres_len >= 2:
                    raise ValidationError('Max genres per band is 2!')


class Rented(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    date_start = models.DateField(default=timezone.now, blank=False)
    date_end = models.DateField(default=month, blank=False)
    returned = models.BooleanField(default=False)

    def clean(self):
        if self.date_start > self.date_end:
            raise ValidationError("End date must be bigger than start date")

