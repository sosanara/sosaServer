from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, AbstractUser
from picture.models import MyResult
# Create your models here.


class MyUser(AbstractUser):
    age = models.IntegerField(blank=False, default=0)
    gender = models.CharField(max_length=2, blank=False, default='0')
    extra = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class MyPicture(models.Model):
    image = models.ImageField(max_length=1024, upload_to='myHair/%Y/%m/%d/%h/%m/%s', blank=False)
    picture = models.ForeignKey(MyUser, related_name="my_user")
    result = models.ForeignKey(MyResult, related_name="my_result")
    extra = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)


