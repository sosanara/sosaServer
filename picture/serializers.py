# -*- coding: utf-8 -*-

from models import MyResult, MyPicture
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _


class MyPictureListSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)

    def validate_image(self, image):
        if image is '':
            raise serializers.ValidationError(_("Image is None. Please insert image"))
        return image

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

    def validate_user(self, user1, user2):
        if user1.id != user2.id:
            raise serializers.ValidationError({"image": _("This image is not yours. Please check your image.")})
        return user1

    def validate_image(self, kwargs):
        my_picture = MyPicture.objects.filter(id=kwargs['picture_id']).first()
        if my_picture == None:
            raise serializers.ValidationError({"image": _("Image was not found.")})
        return my_picture

    def get_cleaned_data(self, user, kwargs):
        my_picture = self.validate_image(kwargs)
        my_user = self.validate_user(user, my_picture.user)
        return {
            'image': my_picture.image.name,
            'result': my_picture.result.image.name,
            'user': my_user.last_name + my_user.first_name,
        }
