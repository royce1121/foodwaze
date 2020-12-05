from django.conf import settings
from django.db import models
from django.utils import timezone
from model_utils.models import TimeStampedModel
from django.utils.translation import gettext as _


class Restaurant(TimeStampedModel):
    RESTAU_TYPE_CHOICES = (
        (1, _("Breakfast")),
        (2, _("Lunch")),
        (3, _("Dinner")),
        (4, _("Cafe")),
        (5, _("Buffet")),
        (6, _("Fine Dining")),
    )

    name = models.CharField(max_length=200)

    description = models.TextField()

    longitude = models.CharField(
        "Longitude of the store",
        max_length=256,
        null=True,
        blank=True,
    )

    latitude = models.CharField(
        "Latitude of the store",
        max_length=256,
        null=True,
        blank=True,
    )

    number_of_visit = models.IntegerField(
        "Number of store",
        null=True,
        blank=True,
    )

    restau_img_url = models.TextField(
        null=True,
        blank=True,
    )

    restau_type = models.IntegerField(
        choices=RESTAU_TYPE_CHOICES,
        default=1,
    )

    def __str__(self):
        return self.name

    def specialty(self):
        menus = Menu.objects.filter(
            restaurant=self,
            is_specialty=True,
        )

        if menus:
            if menus.count() == 1:
                return 'is % s for %s' % (menus.first().name, menus.first().price)
            else:
                string = 'are'
                for menu in menus:
                    string = '%s %s,' % (string, menu.name)
                return string
        return None

    def specialty_menus(self):
        menus = Menu.objects.filter(
            restaurant=self,
            is_specialty=True,
        )

        return menus

    def menus(self):
        menus = Menu.objects.filter(
            restaurant=self,
            is_specialty=False,
        )

        return menus


class Menu(models.Model):
    name = models.CharField(
        "Name of the menu",
        max_length=200,
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1.0
    )

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
    )

    img_url = models.TextField(
        null=True,
        blank=True,
    )

    is_specialty = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return '%s - %s' % (self.name, self.price)


class Visit(TimeStampedModel):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
    )
