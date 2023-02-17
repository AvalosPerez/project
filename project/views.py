from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views import View

from administracion.models import Modulo


class Index(LoginRequiredMixin,View):
    template_name = "home.html"


    def get(self, request, *args, **kwargs):
        context = {}
        #action = request.GET['action']
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        data = {}
        #action = request.POST['action']
        pass
