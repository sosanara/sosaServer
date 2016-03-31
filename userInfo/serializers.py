# -*- coding: utf-8 -*-

from rest_framework import serializers

from .models import MyUser

from django.utils.translation import ugettext_lazy as _


def _validate_user(user1, user2):
    if user1.id != user2.id:
        raise serializers.ValidationError({"user": _("You are not have authorization.")})


def _validate_image(my_picture):
    if my_picture.image is None:
        raise serializers.ValidationError({"image": _("Image was not found.")})


class MyUserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ('username', 'first_name', 'last_name', 'birth', 'gender', 'email')


class MyStaticDetailSerializer(serializers.Serializer):
    def _validate_user(self, all_users):
        if all_users is None:
            raise serializers.ValidationError({"all_users": _("This image is not yours. Please check your image.")})
        # return all_users.


    def _validate_image(self, kwargs):
        my_picture = MyPicture.objects.filter(id=kwargs['picture_id']).first()
        if my_picture is None:
            raise serializers.ValidationError({"image": _("Image was not found.")})
        return {
            'picture': my_picture
        }

    def get_cleaned_data(self, user, all_users):
        self.cleaned_data = self._validate_user(all_users)
        self._validate_user(user, self.cleaned_data['picture'].user)
        return self.cleaned_data['picture']


class MyHistoryListSerializer(serializers.Serializer):

    def get_cleaned_data(self, user, my_pictures):
        pictures = {}
        for my_picture in my_pictures:
            _validate_user(user, my_picture.user)
            _validate_image(my_picture)
            pictures[my_picture.id] = 'uploads/' + my_picture.image.name
        return pictures


class MyHistoryDetailSerializer(serializers.Serializer):

    def get_cleaned_data(self, user, my_picture):
        _validate_user(user, my_picture.user)
        _validate_image(my_picture)
        self.cleaned_data = {
            'name': my_picture.image.name,
            'created_date': my_picture.created_date,
            'type': my_picture.result.type,
        }
        return self.cleaned_data


class MyGraphListSerializer(serializers.Serializer):
    pass


class MyGraphDetailSerializer(serializers.Serializer):
    pass
