# -*- coding: utf-8 -*-

from rest_framework import serializers

from django.utils.translation import ugettext_lazy as _


def _validate_user(user1, user2):
    if user1.id != user2.id:
        raise serializers.ValidationError({"user": _("You are not have authorization.")})


def _validate_image(my_picture):
    if my_picture.image is None:
        raise serializers.ValidationError({"image": _("Image was not found.")})


class MyUserDetailSerializer(serializers.Serializer):
    def get_cleaned_data(self, user):
        self.cleaned_data = {
            'username': user.username,
            'name':  user.last_name + user.first_name,
            'birth': user.birth,
            'gender': user.gender,
            'email': user.email,
        }
        return self.cleaned_data


class MyStaticDetailSerializer(serializers.Serializer):
    # def _validate_user(self, all_users):
    #     if all_users is None:
    #         raise serializers.ValidationError({"all_users": _("This image is not yours. Please check your image.")})
    #     # return all_users.
    #
    #
    # def _validate_image(self, kwargs):
    #     my_picture = MyPicture.objects.filter(id=kwargs['picture_id']).first()
    #     if my_picture is None:
    #         raise serializers.ValidationError({"image": _("Image was not found.")})
    #     return {
    #         'picture': my_picture
    #     }
    #
    # def get_cleaned_data(self, user, all_users):
    #     self.cleaned_data = self._validate_user(all_users)
    #     self._validate_user(user, self.cleaned_data['picture'].user)
    #     return self.cleaned_data['picture']
    pass


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
    def get_cleaned_data(self, user, my_pictures):
        info = {}
        data = {}
        for my_picture in my_pictures:
            _validate_user(user, my_picture.user)
            _validate_image(my_picture)
            data[my_picture.id] = {
                'create_date': my_picture.created_date,
                'birth': my_picture.user.birth,
                'type': my_picture.result.type,
            }
            info.update(data)
        return info


class MyGraphDetailSerializer(serializers.Serializer):
    def get_cleaned_data(self, user, my_picture):
        _validate_user(user, my_picture.user)
        _validate_image(my_picture)
        self.cleaned_data = {
            'image': 'uploads/' + my_picture.image.name,
            'result_image': 'uploads/' + my_picture.result.image.name,
            'result_type': my_picture.result.type,
            'user': my_picture.user.last_name + my_picture.user.first_name,
        }
        return self.cleaned_data
