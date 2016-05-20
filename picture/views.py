# -*- coding: utf-8 -*-

from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import exceptions

from django.utils.translation import ugettext_lazy as _

from .models import MyPicture
from .serializers import MyPictureListSerializer, MyPictureDetailSerializer


def response(picture, message):
    return Response({
            "success": _(message),
            "value": {
                "origin_image": 'uploads/' + picture.origin_image.name,
                "change_image": 'uploads/' + picture.change_image,
                "type": picture.type,
                "percentage": picture.percentage,
                "user": picture.user.last_name + picture.user.first_name,
            }
        })


class PictureList(CreateAPIView):
    serializer_class = MyPictureListSerializer
    permission_classes = (IsAuthenticated,)
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        picture = self.perform_create(serializer)
        return response(picture, "New picture has been saved.")

    def perform_create(self, serializer):
        picture = serializer.save(self.request)
        return picture
