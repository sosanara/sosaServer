# -*- coding: utf-8 -*-
from rest_framework import exceptions
from picture.models import MyPicture
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _


def validate_user(user1, user2):
    if user1.id != user2.id:
        raise serializers.ValidationError({"user": _("You are not have authorization.")})


def validate_image(my_picture):
    if my_picture.origin_image is None:
        raise serializers.ValidationError({"origin_image": _("Image was not found.")})
    if my_picture.change_image is None:
        raise serializers.ValidationError({"change_image": _("Image was not found.")})


class MyUserDetailSerializer(serializers.Serializer):
    def get_cleaned_data(self, user):
        self.cleaned_data = {
            'name':  user.last_name + user.first_name,
            'tutorial': user.tutorial,
        }
        return self.cleaned_data


class MyStaticListSerializer(serializers.Serializer):
    def _get_user(self, all_user):
        type_list = []
        try:
            for user in all_user:
                type_list.append(MyPicture.objects.filter(user_id__exact=user['user_id']).latest('created_date'))
        except MyPicture.DoesNotExist:
            raise exceptions.NotFound()

        return type_list

    def get_cleaned_data(self, all_user, my_last_picture):
        users = self._get_user(all_user)
        age_0, age_1, age_2, age_3, age_4, age_5 = 0, 0, 0, 0, 0, 0
        type_0, type_1, type_2, type_3, type_4 = 0, 0, 0, 0, 0
        cleaned_data = {}

        for user in users:
            validate_image(user)
            age_num = user.age_type
            if age_num == 0: age_0 += 1
            elif age_num == 1: age_1 += 1
            elif age_num == 2: age_2 += 1
            elif age_num == 3: age_3 += 1
            elif age_num == 4: age_4 += 1
            elif age_num == 5: age_5 += 1

            type_num = user.type
            if type_num == 0: type_0 += 1
            elif type_num == 1: type_1 += 1
            elif type_num == 2: type_2 += 1
            elif type_num == 3: type_3 += 1
            elif type_num == 4: type_4 += 1

        cleaned_data.update({
            'age': my_last_picture.created_date.year - my_last_picture.user.birth + 1,
            'ages': {
                '0': age_0,
                '1': age_1,
                '2': age_2,
                '3': age_3,
                '4': age_4,
                '5': age_5,
                'my_age': my_last_picture.age_type,
            },
            'type': {
                '0': type_0,
                '1': type_1,
                '2': type_2,
                '3': type_3,
                '4': type_4,
                'my_type': my_last_picture.type,
            }
        })

        return cleaned_data


class MyGalleryListSerializer(serializers.Serializer):
    def get_cleaned_data(self, user, my_pictures):
        data = {}
        for my_picture in my_pictures:
            validate_user(user, my_picture.user)
            validate_image(my_picture)
            data[my_picture.id] = {
                'origin_image': 'uploads/' + my_picture.origin_image.name,
                'created_data': my_picture.created_date,
            }
        return data


class MyGalleryDetailSerializer(serializers.Serializer):
    def get_cleaned_data(self, user, my_picture):
        validate_user(user, my_picture.user)
        validate_image(my_picture)
        self.cleaned_data = {
            'origin_image_name': my_picture.origin_image.name,
            'change_image_name': my_picture.change_image,
            'type': my_picture.type,
            'percentage': my_picture.percentage,
            'user': my_picture.user.last_name + my_picture.user.first_name,
            'created_date': my_picture.created_date,
        }
        return self.cleaned_data


class MyHistoryListSerializer(serializers.Serializer):
    def get_cleaned_data(self, user, my_pictures):
        data = {}
        for my_picture in my_pictures:
            validate_user(user, my_picture.user)
            validate_image(my_picture)
            data[my_picture.id] = {
                'create_date': my_picture.created_date,
                'birth': my_picture.user.birth,
                'type': my_picture.type,
                'percentage': my_picture.percentage,
            }
        return data


class MyHistoryDetailSerializer(serializers.Serializer):
    def _get_before_picture(self, my_picture):
        before_picture_id = None
        try:
            for picture in MyPicture.objects.filter(user_id=my_picture.user.id):
                if my_picture.id == picture.id:
                    break
                else:
                    before_picture_id = picture.id
            if before_picture_id is None:
                return None
            return MyPicture.objects.get(id=before_picture_id)
        except MyPicture.DoesNotExist:
            raise exceptions.NotFound()

    def _get_first_picture(self, my_picture):
        try:
            first_picture = MyPicture.objects.filter(user_id=my_picture.user.id)[0]
            if my_picture.id == first_picture.id:
                return None
            return first_picture
        except MyPicture.DoesNotExist:
            raise exceptions.NotFound()

    def get_cleaned_data(self, user, my_picture):
        validate_user(user, my_picture.user)
        validate_image(my_picture)
        before = self._get_before_picture(my_picture)
        first = self._get_first_picture(my_picture)

        self.cleaned_data = {
            'current': {
                'origin_image': 'uploads/' + my_picture.origin_image.name,
                'percentage': my_picture.percentage,
                'created_date': my_picture.created_date,
            }
        }

        if before is not None:
            self.cleaned_data.update({
                'before': {
                    'origin_image': 'uploads/' + before.origin_image.name,
                    'percentage': my_picture.percentage - before.percentage,
                    'created_date': before.created_date,
                }
            })

        if first is not None:
            self.cleaned_data.update({
                'first': {
                    'origin_image': 'uploads/' + first.origin_image.name,
                    'percentage': my_picture.percentage - first.percentage,
                    'created_date': first.created_date,
                }
            })

        return self.cleaned_data
