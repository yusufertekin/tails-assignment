from math import radians, cos, sin, asin, sqrt

from django.db import models


class Store(models.Model):
    name = models.TextField()
    postcode = models.CharField(max_length=15)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)

    class Meta:
        indexes = [
            models.Index(fields=('postcode', 'name')),
        ]
