from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from administracion.models import Modulo
from inventario.forms import CategoriaForm, UnidadMedidaForm, InsumoForm, ProveedorForm
from inventario.models import Categoria, UnidadMedida, Insumo, Proveedor


class Index(LoginRequiredMixin, View):
    template_name = "inventario/view.html"
    def get(self, request, *args, **kwargs):
        data = {}
        modulos = Modulo.objects.filter(status = True, activo=True)
        data['modulos'] = modulos
        #action = request.GET['action']
        return render(request, self.template_name, data)

class ViewInsumo(LoginRequiredMixin,ListView):
    template_name = "inventario/insumo/insumo_view.html"
    model = Insumo
    paginate_by = 10
    context_object_name = "insumos"

class AddInsumo(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'inventario.add_insumo'
    model = Insumo
    # fields = ['nombre', 'apellido', 'cedula']
    template_name = "inventario/insumo/addInsumo.html"
    form_class = InsumoForm
    success_url = reverse_lazy('inventario:insumo')
    context_object_name = "insumos"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class EditInsumo(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'inventario.change_insumo'
    model =  Insumo
    template_name = "inventario/insumo/editInsumo.html"
    form_class = InsumoForm
    success_url = reverse_lazy('inventario:insumo')
    context_object_name = "insumos"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class DeleteInsumo(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'inventario.delete_insumo'
    template_name = "inventario/insumo/deleteInsumo.html"
    model = Insumo
    success_url = reverse_lazy('inventario:insumo')
    context_object_name = "insumos"



class ViewProveedor(LoginRequiredMixin,ListView):
    template_name = "inventario/proveedor/view.html"
    model = Proveedor
    paginate_by = 10
    context_object_name = "proveedores"

class AddProveedor(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'inventario.add_proveedor'
    model = Proveedor
    # fields = ['nombre', 'apellido', 'cedula']
    template_name = "inventario/proveedor/addProveedor.html"
    form_class = ProveedorForm
    success_url = reverse_lazy('inventario:proveedor')
    context_object_name = "proveedores"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class EditProveedor(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'inventario.change_proveedor'
    model =  Proveedor
    template_name = "inventario/proveedor/editProveedor.html"
    form_class = ProveedorForm
    success_url = reverse_lazy('inventario:proveedor')
    context_object_name = "proveedores"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class DeleteProveedor(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'inventario.delete_proveedor'
    template_name = "inventario/proveedor/deleteProveedor.html"
    model = Proveedor
    success_url = reverse_lazy('inventario:proveedor')
    context_object_name = "proveedores"





class EntradaInsumo(LoginRequiredMixin, View):
    template_name = "inventario/entrada_insumo_view.html"

    def get(self, request, *args, **kwargs):
        data = {}
        # action = request.GET['action']
        return render(request, self.template_name, data)

    def post(self, request, *args, **kwargs):
        data = {}
        # action = request.POST['action']
        pass

class SalidaInsumo(LoginRequiredMixin, View):
    template_name = "inventario/salida_insumo_view.html"

    def get(self, request, *args, **kwargs):
        data = {}
        # action = request.GET['action']
        return render(request, self.template_name, data)

    def post(self, request, *args, **kwargs):
        data = {}
        # action = request.POST['action']
        pass

class ViewCategoria(LoginRequiredMixin, ListView):
    template_name = "inventario/categoria/categoria_view.html"
    model = Categoria
    paginate_by = 10
    context_object_name = "categorias"

class AddCategoria(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'inventario.add_categoria'
    model = Categoria
    # fields = ['nombre', 'apellido', 'cedula']
    template_name = "inventario/categoria/addCategoria.html"
    form_class = CategoriaForm
    success_url = reverse_lazy('inventario:categoria')
    context_object_name = "categorias"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class EditCategoria(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'inventario.change_categoria'
    model = Categoria
    template_name = "inventario/categoria/editCategoria.html"
    form_class = CategoriaForm
    success_url = reverse_lazy('inventario:categoria')
    context_object_name = "categorias"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class DeleteCategoria(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'inventario.delete_categoria'
    template_name = "inventario/categoria/deleteCategoria.html"
    model = Categoria
    success_url = reverse_lazy('inventario:categoria')



class ViewUnidadMedida(LoginRequiredMixin, ListView):
    template_name = "inventario/unidadMedida/unidad_medida_view.html"
    model = UnidadMedida
    paginate_by = 10
    context_object_name = "unidades_medidas"

class AddUnidadMedida(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'inventario.add_unidadmedida'
    model = UnidadMedida
    # fields = ['nombre', 'apellido', 'cedula']
    template_name = "inventario/unidadMedida/addUnidadMedida.html"
    form_class = UnidadMedidaForm
    success_url = reverse_lazy('inventario:unidad_medida')
    context_object_name = "unidades_medidas"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class EditUnidadMedida(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'inventario.change_unidadmedida'
    model =  UnidadMedida
    template_name = "inventario/unidadMedida/editUnidadMedida.html"
    form_class = UnidadMedidaForm
    success_url = reverse_lazy('inventario:unidad_medida')
    context_object_name = "unidades_medidas"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class DeleteUnidadMedida(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'inventario.delete_unidadmedida'
    template_name = "inventario/unidadMedida/deleteUnidadMedida.html"
    model = UnidadMedida
    success_url = reverse_lazy('inventario:unidad_medida')
    context_object_name = "unidades_medidas"


