from django.urls import path

from administracion.views import Index, ViewModulo, AddModulo, EditModulo, DeleteModulo, ViewUsuario, \
    ViewAccesoModulo, AddAccesoModulo, EditAccesoModulo, DeleteAccesoModulo, \
    ViewCliente, AddCliente, EditCliente, DeleteCliente, AddUsuario, EditUsuario

app_name = 'administracion'
urlpatterns = [
    path('', Index.as_view(), name="administracion"),
    path('modulo/', ViewModulo.as_view(), name="view_modulo"),
    path('modulo/add', AddModulo.as_view(), name="add_modulo"),
    path('modulo/edit/<int:pk>', EditModulo.as_view(), name="edit_modulo"),
    path('modulo/delete/<int:pk>', DeleteModulo.as_view(), name="delete_modulo"),
    path('acceso_modulo/', ViewAccesoModulo.as_view(), name="view_acceso_modulo"),
    path('acceso_modulo/add', AddAccesoModulo.as_view(), name="add_acceso_modulo"),
    path('acceso_modulo/edit/<int:pk>', EditAccesoModulo.as_view(), name="edit_acceso_modulo"),
    path('acceso_modulo/delete/<int:pk>', DeleteAccesoModulo.as_view(), name="delete_acceso_modulo"),
    path('usuario/', ViewUsuario.as_view(), name="view_usuario"),
    path('usuario/add', AddUsuario.as_view(), name="add_usuario"),
    path('usuario/edit/<int:pk>', EditUsuario.as_view(), name="edit_usuario"),
    path('cliente/', ViewCliente.as_view(), name="view_cliente"),
    path('cliente/add', AddCliente.as_view(), name="add_cliente"),
    path('cliente/edit/<int:pk>', EditCliente.as_view(), name="edit_cliente"),
    path('cliente/delete/<int:pk>', DeleteCliente.as_view(), name="delete_cliente"),


]
