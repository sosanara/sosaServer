from django.conf.urls import url, include

from sosaServer.viewset import (
    statistic_list, gallery_list, gallery_detail, history_list, history_detail
)


urlpatterns = [
    url(r'statistic/', include([
        url(r'^$', statistic_list, name="statistic_list"),
    ])),
    url(r'^gallery/', include([
        url(r'^$', gallery_list, name="gallery_list"),
        url(r'^(?P<gallery_id>\d+)/$', gallery_detail, name="gallery_detail"),
    ])),
    url(r'^history/', include([
        url(r'^$', history_list, name="history_list"),
        url(r'^(?P<history_id>\d+)/$', history_detail, name="history_detail"),
    ])),
]
