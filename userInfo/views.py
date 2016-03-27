# Create your views here.

from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from userInfo.models import MyUser
from userInfo.serializers import MyUserSerializer


class TempMixin(object):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer


class UserDetail(TempMixin, RetrieveAPIView):
    serializer_class = MyUserSerializer

    def get_object(self):
        return self.request.user


class StatisticDetail(TempMixin, RetrieveAPIView):
    pass


class GraphViewSet(TempMixin, ReadOnlyModelViewSet):
    pass


class HistoryViewSet(TempMixin, ModelViewSet):
    pass
