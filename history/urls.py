from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from .views import History, ChoiceHistory

urlpatterns = [
    url(r'^$', csrf_exempt(History.as_view()), name="history"),
    url(r'^(?P<history_id>\d+)/$', csrf_exempt(ChoiceHistory.as_view()), name="choice_history"),
]
