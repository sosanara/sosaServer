from django.conf.urls import url

from sosaServer.viewset import (picture_list, picture_detail)


urlpatterns = [
    url(r'^$', picture_list, name="picture_list"),
    url(r'^(?P<picture_id>\d+)/$', picture_detail, name="picture_detail"),
]
