# -*- coding: utf-8 -*-

from rest_framework import serializers

from django.utils.translation import ugettext_lazy as _


def validate_user(user1, user2):
    if user1.id != user2.id:
        raise serializers.ValidationError({"user": _("You are not have authorization.")})


def validate_image(my_picture):
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


class MyStaticListSerializer(serializers.Serializer):
    def get_cleaned_data(self, same_ages, all_ages):
        type_0 = 0
        type_1 = 0
        type_2 = 0
        type_3 = 0
        type_4 = 0
        cleaned_data = {}

        for same_age in same_ages:
            validate_image(same_age)
            type_num = same_age.result.type
            if type_num == 0:
                type_0 += 1
            elif type_num == 1:
                type_1 += 1
            elif type_num == 2:
                type_2 += 1
            elif type_num == 3:
                type_3 += 1
            elif type_num == 4:
                type_4 += 1

        cleaned_data.update({
            'same_ages_type': {
                '0': type_0,
                '1': type_1,
                '2': type_2,
                '3': type_3,
                '4': type_4,
            }
        })

        type_0 = 0
        type_1 = 0
        type_2 = 0
        type_3 = 0
        type_4 = 0

        for all_age in all_ages:
            validate_image(all_age)
            type_num = all_age.result.type
            if type_num == 0:
                type_0 += 1
            elif type_num == 1:
                type_1 += 1
            elif type_num == 2:
                type_2 += 1
            elif type_num == 3:
                type_3 += 1
            elif type_num == 4:
                type_4 += 1

        cleaned_data.update({
            'all_users_type': {
                '0': type_0,
                '1': type_1,
                '2': type_2,
                '3': type_3,
                '4': type_4,
            }
        })

        return cleaned_data


class MyStaticDetailSerializer(serializers.Serializer):
    def _validate_result(self, type):
        if type not in [0, 1, 2, 3, 4]:
            raise serializers.ValidationError({"result": _("Result was not found.")})

    def get_cleaned_data(self, my_result):
        self._validate_result(my_result.type)
        self.cleaned_data = {
            'image': 'uploads/' + my_result.image.name,
            'type': my_result.type,
        }
        return self.cleaned_data


class MyHistoryListSerializer(serializers.Serializer):
    def get_cleaned_data(self, user, my_pictures):
        pictures = {}
        for my_picture in my_pictures:
            validate_user(user, my_picture.user)
            validate_image(my_picture)
            pictures[my_picture.id] = 'uploads/' + my_picture.image.name
        return pictures


class MyHistoryDetailSerializer(serializers.Serializer):
    def get_cleaned_data(self, user, my_picture):
        validate_user(user, my_picture.user)
        validate_image(my_picture)
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
            validate_user(user, my_picture.user)
            validate_image(my_picture)
            data[my_picture.id] = {
                'create_date': my_picture.created_date,
                'birth': my_picture.user.birth,
                'type': my_picture.result.type,
                'percentage': my_picture.result.percentage,
            }
            info.update(data)
        return info


class MyGraphDetailSerializer(serializers.Serializer):
    def get_cleaned_data(self, user, my_picture):
        validate_user(user, my_picture.user)
        validate_image(my_picture)
        self.cleaned_data = {
            'image': 'uploads/' + my_picture.image.name,
            'result_image': 'uploads/' + my_picture.result.image.name,
            'result_type': my_picture.result.type,
            'user': my_picture.user.last_name + my_picture.user.first_name,
        }
        return self.cleaned_data
