from django.conf.urls import url

from sosaServer.viewset import (picture_list, picture_detail)


urlpatterns = [
    url(r'^$', picture_list, name="picture_list"),
]
