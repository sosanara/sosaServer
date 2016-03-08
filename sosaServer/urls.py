"""sosaServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from sosaServer.views import Index, Login, Signup


urlpatterns = [
    url(r'^$', csrf_exempt(Index.as_view()), name="main"),

    url(r'^login/$', csrf_exempt(Login.as_view()), name="login"),
    url(r'^signup/$', csrf_exempt(Signup.as_view()), name="signup"),
    # url(r'^admin/', admin.site.urls, name="admin"),

    url(r'^picture/', include('picture.urls', namespace="picture")),
    url(r'^userInfo/', include('userInfo.urls', namespace="user_info")),
]
