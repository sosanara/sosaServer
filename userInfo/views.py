from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
# Create your views here.


class UserInfo(View):
    def get(self, request):
        return HttpResponse("UserInfo_get")


class Statistic(View):
    def get(self, request):
        return HttpResponse("Statistic_get")


class Graph(View):
    def get(self, request):
        return HttpResponse("Graph_get")


class ChoiceGraph(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("ChoiceGraph_get" + self.kwargs['graph_id'])


class History(View):
    def get(self, request):
        return HttpResponse("History_get")


class ChoiceHistory(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("ChoiceHistory_get" + self.kwargs['history_id'])

    def delete(self, request, *args, **kwargs):
        return HttpResponse("ChoiceHistory_delete, " + self.kwargs['history_id'])
