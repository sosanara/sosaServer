# -*- coding: utf-8 -*-

#  Create your views here.
from pprint import pprint
from datetime import datetime

from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.mixins import DestroyModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK
from rest_framework.viewsets import GenericViewSet
from rest_framework import exceptions

from django.utils.translation import ugettext_lazy as _

from picture.models import MyPicture
from .models import MyUser
from .serializers import MyUserDetailSerializer,\
    MyStaticDetailSerializer,\
    MyGraphListSerializer,\
    MyGraphDetailSerializer,\
    MyHistoryListSerializer,\
    MyHistoryDetailSerializer


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


class StatisticDetail(RetrieveAPIView):
    serializer_class = MyStaticDetailSerializer
    permission_classes = (IsAuthenticated,)
    allowed_methods = ('GET', 'OPTIONS', 'HEAD')

    def get_queryset(self):
        return MyPicture.objects.all().exclude(id=self.request.user_id)

    def get_my_age(self, request):
        pprint(datetime.today().year - request.user.birth)
        return datetime.today().year - request.user.birth

    def get_same_ages(self, my_age):
        filtered_picture = []
        for picture in self.get_queryset():
            if (picture.created_date.year - picture.user.birth)-5 < my_age or \
                                    (picture.created_date.year - picture.user.birth)+5 > my_age:
                filtered_picture.append(picture)

        return filtered_picture

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        my_age = self.get_my_age(request)
        same_ages = self.get_same_ages(my_age)
        statistic = serializer.get_cleaned_data(request.user, self.get_queryset())
        return response(statistic, "It was successful statistic detail search.")


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


class HistoryDetail(RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = MyHistoryDetailSerializer
    permission_classes = (IsAuthenticated,)
    allowed_methods = ('GET', 'DELETE', 'OPTIONS', 'HEAD')

    def get_queryset(self):
        try:
            return MyPicture.objects.get(id=self.kwargs['history_id'])
        except MyPicture.DoesNotExist:
            raise exceptions.NotFound()

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        history_detail = serializer.get_cleaned_data(request.user, self.get_queryset())
        return response(history_detail, "It was successful history detail search.")

    def destroy(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        instance = self.get_queryset()
        history_detail = serializer.get_cleaned_data(request.user, instance)
        self.perform_destroy(instance)
        return response(history_detail, "Successful removed History Parts.", status=HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class GraphList(ListAPIView):
    serializer_class = MyGraphListSerializer
    permission_classes = (IsAuthenticated,)
    allowed_methods = ('GET', 'OPTIONS', 'HEAD')

    def get_queryset(self):
        try:
            return MyUser.objects.get(id=self.request.user.id)
        except MyUser.DoesNotExist:
            raise exceptions.NotFound()

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        graph_list = serializer.get_cleaned_data(request.user, kwargs)
        return response(graph_list, "It was successful graph list search.")


class GraphDetail(RetrieveAPIView):
    serializer_class = MyGraphDetailSerializer
    permission_classes = (IsAuthenticated,)
    allowed_methods = ('GET', 'OPTIONS', 'HEAD')

    def get_queryset(self):
        try:
            return MyUser.objects.get(id=self.request.user.id)
        except MyUser.DoesNotExist:
            raise exceptions.NotFound()

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        graph_detail = serializer.get_cleaned_data(request.user, kwargs)
        return response(graph_detail, "It was successful graph detail search.")
