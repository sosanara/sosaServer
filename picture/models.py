from __future__ import unicode_literals

from django.db import models

# Create your models here.


class MyResult(models.Model):
    image = models.ImageField(max_length=1024, upload_to='myResult/%Y/%m/%d/%h/%m/%s', blank=False)
    type = models.IntegerField(default=0, blank=False)
    extra = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
