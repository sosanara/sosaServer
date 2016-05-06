# -*- coding: utf-8 -*-

#  Create your views here.
from pprint import pprint

from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.mixins import DestroyModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK
from rest_framework.viewsets import GenericViewSet
from rest_framework import exceptions

from django.utils.translation import ugettext_lazy as _

from picture.models import MyPicture, MyResult
from userInfo.models import MyUser

from .serializers import MyUserDetailSerializer,\
    MyStaticListSerializer,\
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
        return response(user_detail, "성공적으로 사용자 데이터를 찾았습니다.")


class StatisticList(ListAPIView):
    serializer_class = MyStaticListSerializer
    permission_classes = (IsAuthenticated,)
    allowed_methods = ('GET', 'OPTIONS', 'HEAD')

    def get_queryset(self):
        return MyPicture.objects.exclude(user_id__exact=self.request.user.id).values('user_id').distinct()

    def get_my_age(self, my_picture):
        return my_picture.created_date.year - self.request.user.birth + 1

    def get_peer_age(self, peer_picture, birth):
        return peer_picture.created_date.year - birth + 1

    def get_peer_max_age(self, my_age):
        return int(my_age / 10) * 10 + 9

    def get_peer_min_age(self, my_age):
        return int(my_age / 10) * 10

    def get_peer(self, my_picture):
        peer_list = []
        my_age = self.get_my_age(my_picture)
        max_age = self.get_peer_max_age(my_age)
        min_age = self.get_peer_min_age(my_age)

        for peer in self.get_queryset():
            peer_picture = MyPicture.objects.filter(user_id__exact=peer['user_id']).latest('created_date')
            peer_age = self.get_peer_age(peer_picture, MyUser.objects.get(id=peer['user_id']).birth)
            if min_age <= peer_age <= max_age:
                peer_list.append(peer_picture)

        return peer_list

    def get_all(self):
        all_list = []
        for part in self.get_queryset():
            part_picture = MyPicture.objects.filter(user_id__exact=part['user_id']).latest('created_date')
            all_list.append(part_picture)
        return all_list

    def get_gender(self):
        gender_list = []
        for part in self.get_queryset():
            try:
                part_picture = MyPicture.objects.filter(
                    user_id__exact=part['user_id'],
                    user__gender__exact=self.request.user.gender,
                ).latest('created_date')
                gender_list.append(part_picture)
            except MyPicture.DoesNotExist:
                pass
        return gender_list

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        my_picture = MyPicture.objects.filter(user_id__exact=self.request.user.id).latest('created_date')
        same_ages = self.get_peer(my_picture)
        all_ages = self.get_all()
        gender_ages = self.get_gender()
        statistic = serializer.get_cleaned_data(same_ages, all_ages, gender_ages)
        statistic.update({
            'my_type': my_picture.result.type
        })

        return response(statistic, "성공적으로 통계 리스트를 찾았습니다.")


class StatisticDetail(RetrieveAPIView):
    serializer_class = MyStaticDetailSerializer
    permission_classes = (IsAuthenticated,)
    allowed_methods = ('GET', 'OPTIONS', 'HEAD')

    def get_queryset(self):
        try:
            return MyResult.objects.filter(type=self.kwargs['statistic_id'])
        except MyResult.DoesNotExist:
            raise exceptions.NotFound()

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        statistic = serializer.get_cleaned_data(self.get_queryset(), self.kwargs['statistic_id'])
        return response(statistic, "성공적으로 통계 데이터를 찾았습니다.")


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
        return response(history_list, "성고적으로 사진첩 리스트를 찾았습니다.")


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
        return response(history_detail, "성공적으로 사진첩 데이터를 찾았습니다.")

    def destroy(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        instance = self.get_queryset()
        history_detail = serializer.get_cleaned_data(request.user, instance)
        self.perform_destroy(instance)
        return response(history_detail, "성공적으로 사진첩 데이터를 지웠습니다.", status=HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class GraphList(ListAPIView):
    serializer_class = MyGraphListSerializer
    permission_classes = (IsAuthenticated,)
    allowed_methods = ('GET', 'OPTIONS', 'HEAD')

    def get_queryset(self):
        try:
            return MyPicture.objects.filter(user=self.request.user)
        except MyPicture.DoesNotExist:
            raise exceptions.NotFound()

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        graph_list = serializer.get_cleaned_data(request.user, self.get_queryset())
        return response(graph_list, "성공적으로 그래프 리스트를 찾았습니다.")


class GraphDetail(RetrieveAPIView):
    serializer_class = MyGraphDetailSerializer
    permission_classes = (IsAuthenticated,)
    allowed_methods = ('GET', 'OPTIONS', 'HEAD')

    def get_queryset(self):
        try:
            return MyPicture.objects.get(id=self.kwargs['graph_id'])
        except MyPicture.DoesNotExist:
            raise exceptions.NotFound()

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        graph_detail = serializer.get_cleaned_data(request.user, self.get_queryset())
        return response(graph_detail, "성공적으로 그래프 데이터를 찾았습니다.")
