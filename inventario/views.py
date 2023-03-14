import xlsxwriter
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, FormView, TemplateView
from inventario.forms import CategoriaForm, UnidadMedidaForm, InsumoForm, ProveedorForm, CompraForm
from inventario.models import Categoria, UnidadMedida, Insumo, Proveedor, Kardex, Compra


class Index(LoginRequiredMixin, ListView):
    template_name = "inventario/view.html"
    model = Kardex
    paginate_by = 10
    context_object_name = "inventario"

    def get_queryset(self):
        query=  Kardex.objects.filter(status=True)
        term = self.request.GET.get('buscar')
        if term:
            query = query.filter(insumo__descripcion__icontains=term) | query.filter(insumo__detalle__icontains=term)
        return query



class AddCompra(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin, CreateView):
    permission_required = 'inventario.add_compra'
    template_name = "inventario/compras/addCompra.html"
    form_class = CompraForm
    success_url = reverse_lazy('inventario:entrada_insumo')
    success_message = 'Registro guardado exitosamente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class EditCompra(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin, UpdateView):
    permission_required = 'inventario.change_compra'
    model = Compra
    template_name = "inventario/compras/editCompra.html"
    form_class = CompraForm
    success_url = reverse_lazy('inventario:entrada_insumo')
    context_object_name = "compras"
    success_message = 'Registro modificado exitosamente'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.usuario_modificacion = self.request.user
        return super().form_valid(form)

class AddDetalleCompraModal(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin, FormView):
    permission_required = 'inventario.add_compra'
    template_name = "inventario/compras/modal/compraFormModal.html"
    form_class = CompraForm
    success_url = reverse_lazy('inventario:entrada_insumo')
    success_message = 'Registro guardado exitosamente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_form']= 'Formulario adicionar compra'
        return context

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        return super().form_valid(form)

def reporte_inventario_xlsx(request):
    # Escribir los datos
    kardexs = Kardex.objects.filter(status=True)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="reporte_inventario.xlsx"'

    workbook = xlsxwriter.Workbook(response, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    # Escribir los encabezados de columna
    encabezados = ['Descripción', 'Unidad de medida', ' Mínimo ', 'Máximo', 'Existencia', 'Entradas', 'Salidas',
                   'Costo', 'Costo total', ]
    for col_num, encabezado in enumerate(encabezados):
        worksheet.write(0, col_num, encabezado)

    for row_num, kardex in enumerate(kardexs):
        worksheet.write(row_num + 1, 0, kardex.insumo.__str__())
        worksheet.write(row_num + 1, 1, kardex.insumo.unidad_medida.__str__())
        worksheet.write(row_num + 1, 2, kardex.insumo.minimo.__str__())
        worksheet.write(row_num + 1, 3, kardex.insumo.maximo.__str__())
        worksheet.write(row_num + 1, 4, kardex.get_existencia().__str__())
        worksheet.write(row_num + 1, 5, kardex.get_inventario_entradas().__str__())
        worksheet.write(row_num + 1, 6, kardex.get_inventario_salidas().__str__())
        worksheet.write(row_num + 1, 7, kardex.get_costo_existencia().__str__())
        worksheet.write(row_num + 1, 8, kardex.get_total_existencia().__str__())

    # Ajustar el ancho de columna
    worksheet.set_column(0, len(encabezados) - 1, 15)

    workbook.close()
    return response

def reporte_movimiento_insumo_xlsx(request, pk):
    insumo = Kardex.objects.get(pk=pk)
    movimientos = insumo.detallekardex_set.filter(status=True)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="reporte_movimientos_insumos.xlsx"'

    workbook = xlsxwriter.Workbook(response, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    #
    merge_format = workbook.add_format({'align': 'center', 'valign': 'vcenter'})

    # Escribir los encabezados de columna
    encabezados = ['Fecha', 'Movimiento', 'Descripción', 'Cantidad', 'Costo', 'Valor', 'Existencia', 'Costo Existencia',
                   'Total existencia', ]
    worksheet.merge_range('A1:I1', 'Detalle de movimiento: ' + insumo.__str__(), merge_format)
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
        context = {}
        kardex = Kardex.objects.get(pk=kwargs['pk'])
        detalleKardex = kardex.detallekardex_set.filter(status=True)
        context['insumo'] = kardex
        context['movimientos'] = detalleKardex
        # action = request.GET['action']
        return render(request, self.template_name, context)

class ViewInsumo(LoginRequiredMixin, ListView):
    template_name = "inventario/insumo/insumo_view.html"
    model = Insumo
    paginate_by = 10
    context_object_name = "insumos"

    def get_queryset(self):
        query= Insumo.objects.filter(status=True)
        term = self.request.GET.get('buscar')
        if term:
            query = query.filter(descripcion__icontains=term) | query.filter(detalle__icontains=term)
        return query

def reporte_insumos_xlsx(request):
    # Escribir los datos
    insumos = Insumo.objects.filter(status=True)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="reporte_insumos.xlsx"'

    workbook = xlsxwriter.Workbook(response, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    # Escribir los encabezados de columna
    encabezados = ['categoria', 'unidad_medida', 'Isumo',
                   'Mínimo', 'Máximo', 'proveedor', 'cantidad', 'Costo unitario' 'Precio Venta', ]
    for col_num, encabezado in enumerate(encabezados):
        worksheet.write(0, col_num, encabezado)

    for row_num, insumo in enumerate(insumos):
        worksheet.write(row_num + 1, 0, insumo.categoria.__str__())
        worksheet.write(row_num + 1, 1, insumo.unidad_medida.__str__())
        worksheet.write(row_num + 1, 2, insumo.descripcion.__str__())
        worksheet.write(row_num + 1, 3, insumo.minimo.__str__())
        worksheet.write(row_num + 1, 4, insumo.maximo.__str__())
        worksheet.write(row_num + 1, 5, insumo.proveedor.__str__())
        worksheet.write(row_num + 1, 6, insumo.cantidad.__str__())
        worksheet.write(row_num + 1, 7, insumo.costo_unitario.__str__())
        worksheet.write(row_num + 1, 8, insumo.precio_venta.__str__())

    # Ajustar el ancho de columna
    worksheet.set_column(0, len(encabezados) - 1, 15)

    workbook.close()
    return response

    # def reporte_insumo_pdf(request):
    #     context = {}
    #     context['insumos']= Insumo.objects.filter(status=True)
    #     html_template = get_template('inventario/report/reporte_insumo_pdf.html').render(context)
    #     pdf_file = HTML(string=html_template, base_url=request.build_absolute_uri(), url_fetcher=url_fetcher).write_pdf()
    #     response = HttpResponse(pdf_file, content_type='application/pdf')
    #     response['Content-Disposition'] = 'inline;filename="reporte_insumo.pdf"'

    return response

class AddInsumo(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin, CreateView):
    permission_required = 'inventario.add_insumo'
    model = Insumo
    # fields = ['nombre', 'apellido', 'cedula']
    template_name = "inventario/insumo/addInsumo.html"
    form_class = InsumoForm
    success_url = reverse_lazy('inventario:insumo')
    context_object_name = "insumos"
    success_message = 'Registro Guardado Exitosamente'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        form.instance.usuario_creacion = self.request.user
        return super().form_valid(form)

class EditInsumo(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin, UpdateView):
    permission_required = 'inventario.change_insumo'
    model = Insumo
    template_name = "inventario/insumo/editInsumo.html"
    form_class = InsumoForm
    success_url = reverse_lazy('inventario:insumo')
    context_object_name = "insumos"
    success_message = 'Registro modificado exitosamente'
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.usuario_modificacion = self.request.user
        return super().form_valid(form)

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

    def get_queryset(self):
        query= Proveedor.objects.filter(status=True)
        term = self.request.GET.get('buscar')
        if term:
            query = query.filter(razon_social__icontains=term) | query.filter(email__icontains=term)
        return query

def reporte_proveedor_xlsx(request):
    # Escribir los datos
    proveedores = Proveedor.objects.filter(status=True)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="reporte_proveedor.xlsx"'

    workbook = xlsxwriter.Workbook(response, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    # Escribir los encabezados de columna
    encabezados = ['Proveedor', 'Email', 'Télefono', ]
    for col_num, encabezado in enumerate(encabezados):
        worksheet.write(0, col_num, encabezado)

    for row_num, proveedor in enumerate(proveedores):
        worksheet.write(row_num + 1, 0, proveedor.razon_social.__str__())
        worksheet.write(row_num + 1, 1, proveedor.email.__str__())
        worksheet.write(row_num + 1, 2, proveedor.telefono.__str__())

    # Ajustar el ancho de columna
    worksheet.set_column(0, len(encabezados) - 1, 15)

    workbook.close()
    return response

class AddProveedor(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin, CreateView):
    permission_required = 'inventario.add_proveedor'
    model = Proveedor
    # fields = ['nombre', 'apellido', 'cedula']
    template_name = "inventario/proveedor/addProveedor.html"
    form_class = ProveedorForm
    success_url = reverse_lazy('inventario:proveedor')
    context_object_name = "proveedores"
    success_message = 'Registro guardado exitosamente'
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.usuario_creacion = self.request.user
        return super().form_valid(form)

class EditProveedor(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin, UpdateView):
    permission_required = 'inventario.change_proveedor'
    model = Proveedor
    template_name = "inventario/proveedor/editProveedor.html"
    form_class = ProveedorForm
    success_url = reverse_lazy('inventario:proveedor')
    context_object_name = "proveedores"
    success_message = 'Registro modificado exitosamente'
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    def form_valid(self, form):
        form.instance.usuario_modificacion = self.request.user
        return super().form_valid(form)

class DeleteProveedor(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'inventario.delete_proveedor'
    template_name = "inventario/proveedor/deleteProveedor.html"
    model = Proveedor
    success_url = reverse_lazy('inventario:proveedor')
    context_object_name = "proveedores"

class EntradaInsumo(LoginRequiredMixin, ListView):
    template_name = "inventario/compras/entrada_insumo_view.html"
    model = Compra
    paginate_by = 10
    context_object_name = "compras"

    def get_queryset(self):
        query= Compra.objects.filter(status=True)
        return query

class SalidaInsumo(LoginRequiredMixin, View):
    template_name = "inventario/ventas/salida_insumo_view.html"

    def get(self, request, *args, **kwargs):
        context = {}
        # action = request.GET['action']
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        # action = request.POST['action']
        pass

class ViewCategoria(LoginRequiredMixin, ListView):
    template_name = "inventario/categoria/categoria_view.html"
    model = Categoria
    paginate_by = 10
    context_object_name = "categorias"

    def get_queryset(self):
        query = Categoria.objects.filter(status=True)
        term = self.request.GET.get('buscar')
        if term:
            query = query.filter(descripcion__icontains=term)
        return query

def reporte_categoria_xlsx(request):
    # Escribir los datos
    categorias = Categoria.objects.filter(status=True)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="reporte_categoria.xlsx"'

    workbook = xlsxwriter.Workbook(response, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    # Escribir los encabezados de columna
    encabezados = ['Categoria', ]
    for col_num, encabezado in enumerate(encabezados):
        worksheet.write(0, col_num, encabezado)

    for row_num, categoria in enumerate(categorias):
        worksheet.write(row_num + 1, 0, categoria.descripcion.__str__())

    # Ajustar el ancho de columna
    worksheet.set_column(0, len(encabezados) - 1, 15)

    workbook.close()
    return response

class AddCategoria(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin, CreateView):
    permission_required = 'inventario.add_categoria'
    model = Categoria
    # fields = ['nombre', 'apellido', 'cedula']
    template_name = "inventario/categoria/addCategoria.html"
    form_class = CategoriaForm
    success_url = reverse_lazy('inventario:categoria')
    context_object_name = "categorias"
    success_message = 'Registro guardado exitosamente'
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    def form_valid(self, form):
        form.instance.usuario_creacion = self.request.user
        return super().form_valid(form)

class EditCategoria(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin, UpdateView):
    permission_required = 'inventario.change_categoria'
    model = Categoria
    template_name = "inventario/categoria/editCategoria.html"
    form_class = CategoriaForm
    success_url = reverse_lazy('inventario:categoria')
    context_object_name = "categorias"
    success_message = 'Registro modificado exitosamente'
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    def form_valid(self, form):
        form.instance.usuario_modificacion = self.request.user
        return super().form_valid(form)

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

    def get_queryset(self):
        query= UnidadMedida.objects.filter(status=True)
        term = self.request.GET.get('buscar')
        if term:
            query = query.filter(descripcion__icontains=term) |query.filter(alias__icontains=term)
        return query

def reporte_unidad_medida_xlsx(request):
    # Escribir los datos
    unidades_de_medidas = UnidadMedida.objects.filter(status=True)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="reporte_unidad_medida.xlsx"'

    workbook = xlsxwriter.Workbook(response, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    # Escribir los encabezados de columna
    encabezados = ['Unidad de medida', 'Alias', ]
    for col_num, encabezado in enumerate(encabezados):
        worksheet.write(0, col_num, encabezado)

    for row_num, unidad in enumerate(unidades_de_medidas):
        worksheet.write(row_num + 1, 0, unidad.descripcion.__str__())
        worksheet.write(row_num + 1, 1, unidad.alias.__str__())

    # Ajustar el ancho de columna
    worksheet.set_column(0, len(encabezados) - 1, 15)

    workbook.close()
    return response

class AddUnidadMedida(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin, CreateView):
    permission_required = 'inventario.add_unidadmedida'
    model = UnidadMedida
    template_name = "inventario/unidadMedida/addUnidadMedida.html"
    form_class = UnidadMedidaForm
    success_url = reverse_lazy('inventario:unidad_medida')
    context_object_name = "unidades_medidas"
    success_message = 'Registro guardado exitosamente'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.usuario_creacion = self.request.user
        return super().form_valid(form)

class EditUnidadMedida(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin, UpdateView):
    permission_required = 'inventario.change_unidadmedida'
    model = UnidadMedida
    template_name = "inventario/unidadMedida/editUnidadMedida.html"
    form_class = UnidadMedidaForm
    success_url = reverse_lazy('inventario:unidad_medida')
    context_object_name = "unidades_medidas"
    success_message = 'Registro modificado exitosamente'
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.usuario_modificacion = self.request.user
        return super().form_valid(form)

class DeleteUnidadMedida(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'inventario.delete_unidadmedida'
    template_name = "inventario/unidadMedida/deleteUnidadMedida.html"
    model = UnidadMedida
    success_url = reverse_lazy('inventario:unidad_medida')
    context_object_name = "unidades_medidas"
