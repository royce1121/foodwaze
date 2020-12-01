from django.conf import settings
from django.db import models
from django.utils import timezone
from model_utils.models import TimeStampedModel

# Create your models here.
class Restaurant(TimeStampedModel):
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

    def __str__(self):
        return self.name