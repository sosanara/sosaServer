from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.
from userInfo.models import MyUser


class MyResult(models.Model):
    image = models.ImageField(max_length=1024, upload_to='myResult/%Y/%m/%d/%h/%m/%s', blank=False)
    type = models.IntegerField(default=0, blank=False, unique=True)
    extra = models.TextField(blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __unicode__(self):
        return self.type


class MyPicture(models.Model):
    image = models.ImageField(max_length=1024, upload_to='myHair/%Y/%m/%d/%h/%m/%s', blank=False)
    user = models.ForeignKey(MyUser, related_name="my_user", blank=False)
    result = models.ForeignKey(MyResult, related_name="my_result", blank=True)
    extra = models.TextField(blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __unicode__(self):
        return self.user
