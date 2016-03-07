from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
# Create your views here.


class Index(View):
    def get(self, request):
        return HttpResponse("Index_get")


class Login(View):
    def get(self, request):
        return HttpResponse("Login_get")

    def post(self, *args, **kwargs):
        return HttpResponse("Login_post")


class Signup(View):
    def get(self, request):
        return HttpResponse("Singup_get")

    def post(self, *args, **kwargs):
        return HttpResponse("Singup_post")
