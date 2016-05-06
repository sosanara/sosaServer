# -*- coding: utf-8 -*-

from .models import MyResult, MyPicture
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _


class MyPictureListSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)

    def validate_image(self, image):
        if image is '':
            raise serializers.ValidationError(_("Image is None. Please insert image"))

    def get_cleaned_data(self, request):
        return {
            'image': request.POST['image'],
            'user': request.user,
            'result': MyResult.objects.get(id='1'),
        }

    def save(self, request):
        self.cleaned_data = self.get_cleaned_data(request)
        return MyPicture.objects.create(
            image=self.cleaned_data['image'],
            user=self.cleaned_data['user'],
            result=self.cleaned_data['result'],
        )


class MyPictureDetailSerializer(serializers.Serializer):
    def _validate_user(self, user1, user2):
        if user1.id != user2.id:
            raise serializers.ValidationError({"user": _("You are not have authorization.")})

    def _validate_image(self, my_picture):
        if my_picture is None:
            raise serializers.ValidationError({"image": _("Image was not found.")})

    def get_cleaned_data(self, user, my_picture):
        self._validate_image(my_picture)
        self._validate_user(user, my_picture.user)
        return my_picture
