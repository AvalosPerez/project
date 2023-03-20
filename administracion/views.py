from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.forms import model_to_dict
# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, UpdateView, CreateView, ListView

from administracion.forms import ModuloForm, GroupAccessForm, ClienteForm, UsuarioForm
from administracion.models import Modulo, GroupAccess
from inventario.models import Usuario, Cliente, Persona


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
    permission_required = 'inventario.view_modulo'
    template_name = "administracion/modulo/view.html"
    model = Modulo
    paginate_by = 10
    context_object_name = "modulos"

    def get_queryset(self):
        query= Modulo.objects.filter(status=True)
        term = self.request.GET.get('buscar')
        if term:
            query = query.filter(nombre__icontains=term) | query.filter(descripcion__icontains=term)
        return query


class AddModulo(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'administracion.add_modulo'
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
    permission_required = 'administracion.change_modulo'
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
    permission_required = 'inventario.view_usuario'
    template_name = "administracion/usuario/view.html"
    model = Usuario
    paginate_by = 10
    context_object_name = "usuarios"

    def get_queryset(self):
        query= Usuario.objects.all()
        term = self.request.GET.get('buscar')
        if term:
            query = query.filter(email__icontains=term) | \
                    query.filter(persona__apellidos__icontains=term)|\
                    query.filter(persona__nombres__icontains=term)|\
                    query.filter(persona__cedula__icontains=term)
        return query

class AddUsuario(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'inventario.add_usuario'
    model = Usuario
    template_name = "administracion/usuario/addUsuario.html"
    form_class = UsuarioForm
    success_url = reverse_lazy('administracion:view_usuario')
    context_object_name = "usuario"

class EditUsuario(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'inventario.change_usuario'
    model = Usuario
    template_name = "administracion/usuario/editUsuario.html"
    form_class = UsuarioForm
    success_url = reverse_lazy('administracion:view_usuario')
    context_object_name = "usuario"


    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Bloquear los campos "cedula" y "email" en el formulario
        form.fields['cedula'].disabled = True
        form.fields['email'].disabled = True
        return form

    def get_initial(self):
        initial = super().get_initial()
        persona = self.object.persona
        initial['nombres'] = persona.nombres
        initial['apellidos'] = persona.apellidos
        initial['email'] = persona.email
        initial['cedula'] = persona.cedula
        return initial

class ViewCliente(LoginRequiredMixin, ListView):
    permission_required = 'inventario.view_cliente'
    template_name = "administracion/cliente/view.html"
    model = Cliente
    paginate_by = 10
    context_object_name = "clientes"

    def get_queryset(self):
        query = Cliente.objects.filter(status=True)
        term = self.request.GET.get('buscar')
        if term:
            query = query.filter(persona__nombres__icontains=term) | query.filter(persona__apellidos__icontains=term) | query.filter(persona__cedula__icontains=term)| query.filter(persona__email__icontains=term)
        return query

class AddCliente(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'inventario.add_cliente'
    model = Cliente
    template_name = "administracion/cliente/addCliente.html"
    form_class = ClienteForm
    success_url = reverse_lazy('administracion:view_cliente')
    context_object_name = "clientes"

    def form_valid(self, form):
        form.instance.usuario_creacion = self.request.user
        return super().form_valid(form)

class EditCliente(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'inventario.change_cliente'
    model = Cliente
    template_name = "administracion/cliente/editCliente.html"
    form_class = ClienteForm
    success_url = reverse_lazy('administracion:view_cliente')
    context_object_name = "clientes"


    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Bloquear los campos "cedula" y "email" en el formulario
        form.fields['cedula'].disabled = True
        form.fields['email'].disabled = True
        return form

    def get_initial(self):
        initial = super().get_initial()
        persona = self.object.persona
        initial['nombres'] = persona.nombres
        initial['apellidos'] = persona.apellidos
        initial['email'] = persona.email
        initial['cedula'] = persona.cedula
        return initial


    def form_valid(self, form):
        form.instance.usuario_modificacion = self.request.user
        return super().form_valid(form)

class DeleteCliente(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'inventario.delete_cliente'
    template_name = "administracion/cliente/deleteCliente.html"
    model = Cliente
    success_url = reverse_lazy('administracion:view_cliente')
    context_object_name = "clientes"

class ViewAccesoModulo(LoginRequiredMixin, ListView):
    permission_required = 'administracion.view_groupaccess'
    template_name = "administracion/acceso_modulo/view.html"
    model = GroupAccess
    paginate_by = 10
    context_object_name = "acceso_modulo"

    def get_queryset(self):
        query= GroupAccess.objects.filter(status=True)

        return query

class AddAccesoModulo(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'administracion.add_groupaccess'
    model = GroupAccess
    template_name = "administracion/acceso_modulo/add_acceso_modulo.html"
    form_class = GroupAccessForm
    success_url = reverse_lazy('administracion:view_acceso_modulo')
    context_object_name = "acceso_modulo"

    def form_valid(self, form):
        form.instance.usuario_creacion = self.request.user
        return super().form_valid(form)

class EditAccesoModulo(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'administracion.change_groupaccess'
    model = GroupAccess
    template_name = "administracion/acceso_modulo/edit_acceso_modulo.html"
    form_class = GroupAccessForm
    success_url = reverse_lazy('administracion:view_acceso_modulo')
    context_object_name = "acceso_modulo"

    def form_valid(self, form):
        form.instance.usuario_modificacion = self.request.user
        return super().form_valid(form)

class DeleteAccesoModulo(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'administracion.delete_groupaccess'
    template_name = "administracion/acceso_modulo/delete_acceso_modulo.html"
    model = GroupAccess
    success_url = reverse_lazy('administracion:view_acceso_modulo')
    context_object_name = "acceso_modulo"

class ViewGrupo(LoginRequiredMixin, ListView):
    template_name = "administracion/grupos/view.html"
    model = Group
    paginate_by = 10
    context_object_name = "grupo"
