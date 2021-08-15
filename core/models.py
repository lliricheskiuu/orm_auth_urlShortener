from django.db import models
from django.utils.baseconv import base56
import random


MIN_KEY, MAX_KEY = 80106440, 550731775


class Url(models.Model):
    key = models.SlugField(unique=True)
    url = models.URLField()
    redirect_count = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.key = base56.encode(random.randint(MIN_KEY, MAX_KEY))
            self.redirect_count = 0
        super().save(*args, **kwargs)