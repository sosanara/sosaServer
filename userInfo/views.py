# -*- coding: utf-8 -*-

#  Create your views here.

from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.mixins import DestroyModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK
from rest_framework.viewsets import GenericViewSet
from rest_framework import exceptions

from django.utils.translation import ugettext_lazy as _

from picture.models import MyPicture

from .serializers import MyUserDetailSerializer,\
    MyStaticListSerializer,\
    MyHistoryListSerializer,\
    MyHistoryDetailSerializer,\
    MyGalleryListSerializer,\
    MyGalleryDetailSerializer


def response(value, message, status=HTTP_200_OK):
    return Response({
            "success": _(message),
            "value": value
        }, status=status)


class UserDetail(RetrieveAPIView):
    serializer_class = MyUserDetailSerializer
    permission_classes = (IsAuthenticated,)
    allowed_methods = ('GET', 'OPTIONS', 'HEAD')

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user_detail = serializer.get_cleaned_data(self.get_object())
        return response(user_detail, "It was successful user detail search.")


class StatisticList(ListAPIView):
    serializer_class = MyStaticListSerializer
    permission_classes = (IsAuthenticated,)
    allowed_methods = ('GET', 'OPTIONS', 'HEAD')

    def get_queryset(self):
        try:
            return MyPicture.objects.all().values('user_id').distinct()
        except MyPicture.DoesNotExist:
            raise exceptions.NotFound()

    def get_last_image(self):
        try:
            return MyPicture.objects.filter(user_id__exact=self.request.user.id).latest('created_date')
        except MyPicture.DoesNotExist:
            raise exceptions.NotFound()

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        all_user = self.get_queryset()
        my_last_picture = self.get_last_image()
        statistic = serializer.get_cleaned_data(all_user, my_last_picture)

        return response(statistic, "It was successful statistic list search.")


class GalleryList(ListAPIView):
    serializer_class = MyGalleryListSerializer
    permission_classes = (IsAuthenticated,)
    allowed_methods = ('GET', 'OPTIONS', 'HEAD')

    def get_queryset(self):
        try:
            return MyPicture.objects.filter(user=self.request.user)
        except MyPicture.DoesNotExist:
            raise exceptions.NotFound()

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        gallery_list = serializer.get_cleaned_data(request.user, self.get_queryset())
        return response(gallery_list, "It was successful gallery list search.")


class GalleryDetail(RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = MyGalleryDetailSerializer
    permission_classes = (IsAuthenticated,)
    allowed_methods = ('GET', 'DELETE', 'OPTIONS', 'HEAD')

    def get_queryset(self):
        try:
            return MyPicture.objects.get(id=self.kwargs['gallery_id'])
        except MyPicture.DoesNotExist:
            raise exceptions.NotFound()

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        gallery_detail = serializer.get_cleaned_data(request.user, self.get_queryset())
        return response(gallery_detail, "It was successful gallery detail search.")

    def destroy(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        instance = self.get_queryset()
        gallery_detail = serializer.get_cleaned_data(request.user, instance)
        self.perform_destroy(instance)
        return response(gallery_detail, "Successful removed Gallery Parts.", status=HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class HistoryList(ListAPIView):
    serializer_class = MyHistoryListSerializer
    permission_classes = (IsAuthenticated,)
    allowed_methods = ('GET', 'OPTIONS', 'HEAD')

    def get_queryset(self):
        try:
            return MyPicture.objects.filter(user=self.request.user)
        except MyPicture.DoesNotExist:
            raise exceptions.NotFound()

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        history_list = serializer.get_cleaned_data(request.user, self.get_queryset())
        return response(history_list, "It was successful history list search.")


class HistoryDetail(RetrieveAPIView):
    serializer_class = MyHistoryDetailSerializer
    permission_classes = (IsAuthenticated,)
    allowed_methods = ('GET', 'OPTIONS', 'HEAD')

    def get_queryset(self):
        try:
            return MyPicture.objects.get(id=self.kwargs['history_id'])
        except MyPicture.DoesNotExist:
            raise exceptions.NotFound()

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        history_detail = serializer.get_cleaned_data(request.user, self.get_queryset())
        return response(history_detail, "It was successful history detail search.")
