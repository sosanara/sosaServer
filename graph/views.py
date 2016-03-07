from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
# Create your views here.


class Graph(View):
    def get(self, request):
        return HttpResponse("Graph_get")


class ChoiceGraph(View):
    def get(self, request):
        return HttpResponse("ChoiceGraph_get")

