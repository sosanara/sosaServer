# -*- coding: utf-8 -*-
from .models import MyPicture
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

from ML import SVM, GetBinaryImage

from conf.machineLearning import reference_image, learn_data


class MyPictureListSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)

    def validate_image(self, image):
        if image is '':
            raise serializers.ValidationError(_("Image is None. Please insert image"))

    def get_cleaned_data(self, request):
        return {
            'image': request.POST['image'],
            'user': request.user,
        }

    def _get_age(self, picture):
        return picture.created_date.year - picture.user.birth + 1

    def _get_removed_filename(self, input_path):
        return input_path[:-len(input_path.split('/')[-1])]

    def _get_ml_image(self, path):
        binary_image = GetBinaryImage.BImage('uploaded_files/' + path)
        return binary_image.save_binary_to_image(
            'uploaded_files/' + self._get_removed_filename(path), 1, 180, 100
        )

    def _get_ml_result(self, path):
        return SVM.BSVM.get_bald_SVM('uploaded_files/' + path, reference_image(), learn_data())

    def _set_age_type(self, picture):
        my_age = self._get_age(picture)
        if 20 > my_age:
            return 0
        if 20 <= my_age < 29:
            return 1
        if 30 <= my_age < 39:
            return 2
        if 40 <= my_age < 49:
            return 3
        if 50 <= my_age < 59:
            return 4
        if my_age >= 59:
            return 5

    def _set_tutorial(self, user):
        user.tutorial = True
        user.save()

    def save(self, request):
        self.cleaned_data = self.get_cleaned_data(request)

        my_picture = MyPicture.objects.create(
            origin_image=self.cleaned_data['image'],
            user=self.cleaned_data['user'],
        )

        ml = self._get_ml_result(my_picture.origin_image.name)
        ml_image = self._get_ml_image(my_picture.origin_image.name)

        my_picture.age_type = self._set_age_type(my_picture)
        my_picture.change_image = ml_image['fullname'][len(ml_image['fullname'].split('/')[0])+1:]
        my_picture.type = ml['result']['type']
        my_picture.percentage = ml['result']['percent']
        if my_picture.user.tutorial is False:
            self._set_tutorial(request.user)
        my_picture.save()
        return my_picture
