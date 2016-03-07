from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from .views import Picture, ChoicePicture

urlpatterns = [
    url(r'^$', csrf_exempt(Picture.as_view()), name="picture"),
    url(r'^(?P<picture_id>\d+)/$', csrf_exempt(ChoicePicture.as_view()), name="choice_picture"),
]
