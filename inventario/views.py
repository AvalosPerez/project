from typing import io

import xlsxwriter
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from administracion.models import Modulo
from inventario.forms import CategoriaForm, UnidadMedidaForm, InsumoForm, ProveedorForm
from inventario.models import Categoria, UnidadMedida, Insumo, Proveedor, Kardex, DetalleKardex


class Index(LoginRequiredMixin, View):
    template_name = "inventario/view.html"

    def get(self, request, *args, **kwargs):
        data = {}
        inventario = Kardex.objects.filter(status=True)
        data['inventario'] = inventario
        # action = request.GET['action']
        return render(request, self.template_name, data)


def reporte_movimiento_insumo_xlsx(request, pk):
    insumo = Kardex.objects.get(pk=pk)
    movimientos = insumo.detallekardex_set.filter(status=True)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="reporte_movimientos_insumos.xlsx"'

    workbook = xlsxwriter.Workbook(response, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    #
    merge_format = workbook.add_format({ 'align': 'center', 'valign': 'vcenter' })

    # Escribir los encabezados de columna
    encabezados = ['Fecha', 'Movimiento', 'Descripción', 'Cantidad', 'Costo', 'Valor', 'Existencia', 'Costo Existencia', 'Total existencia', ]
    worksheet.merge_range('A1:I1', 'Detalle de movimiento: '+insumo.__str__(), merge_format)
    for col_num, encabezado in enumerate(encabezados):
        worksheet.write(1, col_num, encabezado)

    for row_num, movimiento in enumerate(movimientos):
        worksheet.write(row_num + 2, 0, movimiento.fecha.__str__())
        worksheet.write(row_num + 2, 1, movimiento.get_tipo_movimiento_display().__str__())
        worksheet.write(row_num + 2, 2, movimiento.detalle.__str__())
        worksheet.write(row_num + 2, 3, movimiento.cantidad.__str__())
        worksheet.write(row_num + 2, 4, movimiento.costo_unitario.__str__())
        worksheet.write(row_num + 2, 5, movimiento.importe.__str__())
        worksheet.write(row_num + 2, 6, movimiento.cantidad_anterior.__str__())
        worksheet.write(row_num + 2, 7, movimiento.costo_anterior.__str__())
        worksheet.write(row_num + 2, 8, movimiento.import_anterior.__str__())

    # Ajustar el ancho de columna
    worksheet.set_column(0, len(encabezados) - 1, 15)

    workbook.close()
    return response


class MovimientoView(LoginRequiredMixin, View):
    template_name = "inventario/movimientoView.html"

    def get(self, request, *args, **kwargs):
        data = {}
        kardex = Kardex.objects.get(pk=kwargs['pk'])
        detalleKardex = kardex.detallekardex_set.filter(status=True)
        data['insumo'] = kardex
        data['movimientos'] = detalleKardex
        # action = request.GET['action']
        return render(request, self.template_name, data)


class ViewInsumo(LoginRequiredMixin, ListView):
    template_name = "inventario/insumo/insumo_view.html"
    model = Insumo
    paginate_by = 10
    context_object_name = "insumos"

    def get(self, request, *args, **kwargs):
        return super().get(request)


def reporte_insumos_xlsx(request):
    # Escribir los datos
    insumos = Insumo.objects.filter(status=True)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="reporte_insumos.xlsx"'

    workbook = xlsxwriter.Workbook(response, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    # Escribir los encabezados de columna
    encabezados = ['categoria', 'unidad_medida', 'lote', 'Isumo', 'presentacion_comercial', 'fecha_vencimiento',
                   'Mínimo', 'Máximo', 'proveedor', 'cantidad', 'Costo unitario' 'Precio Venta', ]
    for col_num, encabezado in enumerate(encabezados):
        worksheet.write(0, col_num, encabezado)

    for row_num, insumo in enumerate(insumos):
        worksheet.write(row_num + 1, 0, insumo.categoria.__str__())
        worksheet.write(row_num + 1, 1, insumo.unidad_medida.__str__())
        worksheet.write(row_num + 1, 2, insumo.lote.__str__())
        worksheet.write(row_num + 1, 3, insumo.descripcion.__str__())
        worksheet.write(row_num + 1, 4, insumo.presentacion_comercial.__str__())
        worksheet.write(row_num + 1, 5, insumo.fecha_vencimiento.__str__())
        worksheet.write(row_num + 1, 6, insumo.minimo.__str__())
        worksheet.write(row_num + 1, 7, insumo.maximo.__str__())
        worksheet.write(row_num + 1, 8, insumo.proveedor.__str__())
        worksheet.write(row_num + 1, 9, insumo.cantidad.__str__())
        worksheet.write(row_num + 1, 10, insumo.costo_unitario.__str__())
        worksheet.write(row_num + 1, 11, insumo.precio_venta.__str__())

    # Ajustar el ancho de columna
    worksheet.set_column(0, len(encabezados) - 1, 15)

    workbook.close()
    return response


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

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        self.object.generar_inventario_inicial()
        return super().form_valid(form)


class EditInsumo(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'inventario.change_insumo'
    model = Insumo
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


class ViewProveedor(LoginRequiredMixin, ListView):
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
    model = Proveedor
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
    model = UnidadMedida
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
