from django.conf.urls import url, include

from sosaServer.viewset import (
    statistic_list, statistic_detail, graph_list, graph_detail, history_list, history_detail
)


urlpatterns = [
    url(r'statistic/', include([
        url(r'^$', statistic_list, name="statistic_list"),
        url(r'^(?P<statistic_id>\d+)/$', statistic_detail, name="statistic_detail"),
    ])),
    url(r'^graph/', include([
        url(r'^$', graph_list, name="graph_list"),
        url(r'^(?P<graph_id>\d+)/$', graph_detail, name="graph_detail"),
    ])),
    url(r'^history/', include([
        url(r'^$', history_list, name="history_list"),
        url(r'^(?P<history_id>\d+)/$', history_detail, name="history_detail"),
    ])),
]
