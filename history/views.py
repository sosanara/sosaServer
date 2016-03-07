from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
# Create your views here.


class History(View):
    def get(self, request):
        return HttpResponse("History_get")


class ChoiceHistory(View):
    def get(self, request):
        return HttpResponse("ChoiceHistory_get" + self.kwargs['history_id'])

    def delete(self, request, *args, **kwargs):
        return HttpResponse("ChoiceHistory_delete, " + self.kwargs['history_id'])
