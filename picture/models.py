from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
from userInfo.models import MyUser


def user_directory_path(instance, filename):
    return 'myHair/{0}/{1}.{2}'.format(datetime.datetime.strftime(datetime.datetime.now(), "%Y/%m/%d/%h/%m/%s"),
                                       instance.user.id, filename.split('.')[-1])


class MyPicture(models.Model):
    origin_image = models.ImageField(max_length=1024, upload_to=user_directory_path, blank=False)
    change_image = models.TextField(blank=True)
    user = models.ForeignKey(MyUser, related_name="my_user", blank=False)
    type = models.IntegerField(default=0, blank=False)
    age_type = models.IntegerField(default=0, blank=False)
    percentage = models.FloatField(default=0, blank=False)
    product = models.TextField(blank=True)
    advice = models.TextField(blank=True)
    extra = models.TextField(blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __unicode__(self):
        return self.user
