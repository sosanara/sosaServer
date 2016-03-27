from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone

# Create your models here.
from rest_framework.authtoken.models import Token


class MyUser(AbstractUser):
    birth = models.IntegerField(blank=False, default=0)
    gender = models.CharField(max_length=10, blank=False, default='0')
    extra = models.TextField(blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now, blank=True, null=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __unicode__(self):
        return self.username
