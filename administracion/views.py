from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, UpdateView, CreateView, ListView

from administracion.forms import ModuloForm
from administracion.models import Modulo


class Index(LoginRequiredMixin,View):
    template_name = "administracion/view.html"


    def get(self, request, *args, **kwargs):
        data = {}
        modulos = Modulo.objects.filter(status = True, activo=True)
        data['modulos'] = modulos
        #action = request.GET['action']
        return render(request, self.template_name, data)

    def post(self, request, *args, **kwargs):
        data = {}
        #action = request.POST['action']
        pass



class ViewModulo(LoginRequiredMixin,ListView):
    template_name = "administracion/modulo/view.html"
    model = Modulo
    paginate_by = 10
    context_object_name = "modulos"

class AddModulo(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'inventario.add_modulo'
    model = Modulo
    # fields = ['nombre', 'apellido', 'cedula']
    template_name = "administracion/modulo/addModulo.html"
    form_class = ModuloForm
    success_url = reverse_lazy('administracion:view_modulo')
    context_object_name = "modulos"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class EditModulo(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'inventario.change_modulo'
    model =  Modulo
    template_name = "administracion/modulo/editModulo.html"
    form_class = ModuloForm
    success_url = reverse_lazy('administracion:view_modulo')
    context_object_name = "modulos"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class DeleteModulo(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'inventario.delete_modulo'
    template_name = "administracion/modulo/deleteModulo.html"
    model = Modulo
    success_url = reverse_lazy('administracion:view_modulo')
    context_object_name = "modulos"