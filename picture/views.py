from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
# Create your views here.


class Picture(View):
    def get(self, request):
        return HttpResponse("Picture_get")

    def post(self, request, *args, **kwargs):
        return HttpResponse("Picture_post")


class ChoicePicture(View):
    def get(self, request):
        return HttpResponse("ChoicePicture_get")
