from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt
from .views import UserInfo, Graph, ChoiceGraph, History, ChoiceHistory

urlpatterns = [
    url(r'^$', csrf_exempt(UserInfo.as_view()), name="user_info"),

    url(r'^graph/', include([
        url(r'^$', csrf_exempt(Graph.as_view()), name="graph"),
        url(r'^(?P<graph_id>\d+)/$', csrf_exempt(ChoiceGraph.as_view()), name="choice_graph"),
    ])),
    url(r'^history/', include([
        url(r'^$', csrf_exempt(History.as_view()), name="history"),
        url(r'^(?P<history_id>\d+)/$', csrf_exempt(ChoiceHistory.as_view()), name="choice_history"),
    ])),
]
