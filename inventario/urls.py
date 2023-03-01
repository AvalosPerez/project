from django.urls import path

from inventario.views import Index, ViewInsumo, EntradaInsumo, SalidaInsumo, ViewCategoria, ViewUnidadMedida, \
    AddCategoria, \
    EditCategoria, DeleteCategoria, AddUnidadMedida, EditUnidadMedida, DeleteUnidadMedida, AddInsumo, EditInsumo, \
    DeleteInsumo, ViewProveedor, AddProveedor, EditProveedor, DeleteProveedor, MovimientoView, reporte_insumos_xlsx, \
    reporte_movimiento_insumo_xlsx, reporte_proveedor_xlsx, reporte_categoria_xlsx, \
    reporte_unidad_medida_xlsx, reporte_inventario_xlsx, AddCompra, EditCompra

app_name = 'inventario'
urlpatterns = [
    path('', Index.as_view(), name="inventario"),
    path('movimientos/<int:pk>', MovimientoView.as_view(), name="movimiento"),
    path('entradas/', EntradaInsumo.as_view(), name="entrada_insumo"),
    path('entradas/add/', AddCompra.as_view(), name="add_compra"),
    path('entradas/edit/<int:pk>', EditCompra.as_view(), name="edit_compra"),
    path('salidas/', SalidaInsumo.as_view(), name="salida_insumo"),
    path('insumos/', ViewInsumo.as_view(), name="insumo"),
    path('insumos/add/', AddInsumo.as_view(), name="add_insumo"),
    path('insumos/edit/<int:pk>', EditInsumo.as_view(), name="edit_insumo"),
    path('insumos/delete/<int:pk>', DeleteInsumo.as_view(), name="delete_insumo"),
    path('insumos/categoria/', ViewCategoria.as_view(), name="categoria"),
    path('insumos/categoria/add/', AddCategoria.as_view(), name="add_categoria"),
    path('insumos/categoria/edit/<int:pk>', EditCategoria.as_view(), name="edit_categoria"),
    path('insumos/categoria/delete/<int:pk>', DeleteCategoria.as_view(), name="delete_categoria"),
    path('insumos/unidadMedida/', ViewUnidadMedida.as_view(), name="unidad_medida"),
    path('insumos/unidadMedida/add/', AddUnidadMedida.as_view(), name="add_unidad_medida"),
    path('insumos/unidadMedida/edit/<int:pk>', EditUnidadMedida.as_view(), name="edit_unidad_medida"),
    path('insumos/unidadMedida/delete/<int:pk>', DeleteUnidadMedida.as_view(), name="delete_unidad_medida"),
    path('insumos/proveedor/', ViewProveedor.as_view(), name="proveedor"),
    path('insumos/proveedor/add/', AddProveedor.as_view(), name="add_proveedor"),
    path('insumos/proveedor/edit/<int:pk>', EditProveedor.as_view(), name="edit_proveedor"),
    path('insumos/proveedor/delete/<int:pk>', DeleteProveedor.as_view(), name="delete_proveedor"),
    path('insumos/reporte_insumo_xlsx/', reporte_insumos_xlsx, name='reporte_insumos_xlsx'),
    path('reporte_movimiento_xlsx/<int:pk>', reporte_movimiento_insumo_xlsx, name='reporte_movimiento_insumo_xlsx'),
    #path('reporte_insumo_pdf', reporte_insumo_pdf, name="reporte_insumo_pdf" ),
    path('reporte_proveedor_xlsx/', reporte_proveedor_xlsx, name='reporte_proveedor_xlsx'),
    path('reporte_categoria_xlsx/', reporte_categoria_xlsx, name='reporte_categoria_xlsx'),
    path('reporte_unidad_medida_xlsx/', reporte_unidad_medida_xlsx, name='reporte_unidad_medida_xlsx'),
    path('reporte_unidad_medida_xlsx/', reporte_unidad_medida_xlsx, name='reporte_unidad_medida_xlsx'),
    path('reporte_inventario_xlsx/', reporte_inventario_xlsx, name='reporte_inventario_xlsx'),

]
