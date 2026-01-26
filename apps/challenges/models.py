from django.db import models
from apps.core.mixins import JsonQueryMixin

class Gadget(JsonQueryMixin, models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    specs = models.JSONField(default=dict)  # Hardver specifikációk tárolása
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name