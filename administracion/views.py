from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.forms import model_to_dict
# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, UpdateView, CreateView, ListView

from administracion.forms import ModuloForm, UsuarioForm, PersonaForm
from administracion.models import Modulo
from inventario.models import Usuario, Persona


class Index(LoginRequiredMixin, View):
    template_name = "administracion/view.html"

    def get(self, request, *args, **kwargs):
        data = {}
        modulos = Modulo.objects.filter(status=True, activo=True)
        data['modulos'] = modulos
        # action = request.GET['action']
        return render(request, self.template_name, data)

    def post(self, request, *args, **kwargs):
        data = {}
        # action = request.POST['action']
        pass


class ViewModulo(LoginRequiredMixin, ListView):
    template_name = "administracion/modulo/view.html"
    model = Modulo
    paginate_by = 10
    context_object_name = "modulos"

    def get_queryset(self):
        query= Modulo.objects.filter(status=True)
        return query


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

    def form_valid(self, form):
        form.instance.usuario_creacion = self.request.user
        return super().form_valid(form)


class EditModulo(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'inventario.change_modulo'
    model = Modulo
    template_name = "administracion/modulo/editModulo.html"
    form_class = ModuloForm
    success_url = reverse_lazy('administracion:view_modulo')
    context_object_name = "modulos"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.usuario_modificacion = self.request.user
        return super().form_valid(form)


class DeleteModulo(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'administracion.delete_modulo'
    template_name = "administracion/modulo/deleteModulo.html"
    model = Modulo
    success_url = reverse_lazy('administracion:view_modulo')
    context_object_name = "modulos"



class ViewUsuario(LoginRequiredMixin, ListView):
    template_name = "administracion/usuario/view.html"
    model = Usuario
    paginate_by = 10
    context_object_name = "usuarios"

class ViewPersona(LoginRequiredMixin, ListView):
    template_name = "administracion/persona/view.html"
    model = Persona
    paginate_by = 10
    context_object_name = "personas"

    def get_queryset(self):
        query = Persona.objects.filter(status=True)
        return query


class AddPersona(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'inventario.add_persona'
    model = Persona
    template_name = "administracion/persona/addPersona.html"
    form_class = PersonaForm
    success_url = reverse_lazy('administracion:view_persona')
    context_object_name = "personas"

    def form_valid(self, form):
        form.instance.usuario_creacion = self.request.user
        return super().form_valid(form)


class EditPersona(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'inventario.change_persona'
    model = Persona
    template_name = "administracion/persona/editPersona.html"
    form_class = PersonaForm
    success_url = reverse_lazy('administracion:view_persona')
    context_object_name = "personas"

    def form_valid(self, form):
        form.instance.usuario_modificacion = self.request.user
        return super().form_valid(form)


class DeletePersona(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'inventario.delete_persona'
    template_name = "administracion/persona/deletePersona.html"
    model = Persona
    success_url = reverse_lazy('administracion:view_persona')
    context_object_name = "personas"

#
# class ViewEmpresa(LoginRequiredMixin, ListView):
#     template_name = "administracion/empresa/view.html"
#     model = Empresa
#     paginate_by = 10
#     context_object_name = "empresas"
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         #
#         mi_empresa = Empresa.objects.filter(status=True)
#         context['existe_mi_empresa'] = mi_empresa.exists()
#
#         if mi_empresa.exists():
#             context['datos_empresa'] = mi_empresa[0]
#             context['form'] = EmpresaForm(initial=model_to_dict(mi_empresa[0]))
#         else:
#             context['form'] = EmpresaForm
#         return context
#
#
# class AddEmpresa(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
#     permission_required = 'inventario.add_empresa'
#     model = Empresa
#     template_name = "administracion/empresa/addEmpresa.html"
#     form_class = EmpresaForm
#     success_url = reverse_lazy('administracion:view_empresa')
#     context_object_name = "empresas"
#
#     def form_valid(self, form):
#         form.instance.usuario_creacion = self.request.user
#         return super().form_valid(form)
#
#
# class EditEmpresa(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
#     permission_required = 'inventario.change_empresa'
#     model = Empresa
#     template_name = "administracion/empresa/editEmpresa.html"
#     form_class = EmpresaForm
#     success_url = reverse_lazy('administracion:view_empresa')
#     context_object_name = "empresas"
#
#     def form_valid(self, form):
#         form.instance.usuario_modificacion = self.request.user
#         return super().form_valid(form)
#
#
# class DeleteEmpresa(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
#     permission_required = 'inventario.delete_empresa'
#     template_name = "administracion/empresa/deleteEmpresa.html"
#     model = Empresa
#     success_url = reverse_lazy('administracion:view_empresa')
#     context_object_name = "empresas"
