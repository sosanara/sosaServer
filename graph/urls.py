from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from .views import Graph, ChoiceGraph

urlpatterns = [
    url(r'^$', csrf_exempt(Graph.as_view()), name="graph"),
    url(r'^(?P<graph_id>\d+)/$', csrf_exempt(ChoiceGraph.as_view()), name="choice_graph"),
]
