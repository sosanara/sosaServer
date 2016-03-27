# -*- coding: utf-8 -*-
from pprint import pprint

from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.utils.translation import ugettext_lazy as _

from picture.models import MyPicture
from picture.serializers import MyPictureListSerializer, MyPictureDetailSerializer


class TempMixin(object):
    permission_classes = (IsAuthenticated,)


##### OpenCV 연산을 여기서 해야됨. #####
class PictureList(TempMixin, CreateAPIView):
    serializer_class = MyPictureListSerializer
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        picture = self.perform_create(serializer)

        return Response({
            "success": _("New picture has been saved."),
            "value": {
                "image": picture.image.name,
                "result": picture.result.image.name,
                "user": picture.user.last_name + picture.user.first_name,
            }
        })

    def perform_create(self, serializer):
        picture = serializer.save(self.request)
        return picture


class PictureDetail(TempMixin, RetrieveAPIView):
    serializer_class = MyPictureDetailSerializer
    allowed_methods = ('GET', 'OPTIONS', 'HEAD')

    def get_queryset(self):
        return MyPicture.objects.get(id=self.kwargs['picture_id'])

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        picture = serializer.get_cleaned_data(request.user, kwargs)

        return Response({
            "success": _("Saved picture has been retrieved."),
            "value": picture
        })
