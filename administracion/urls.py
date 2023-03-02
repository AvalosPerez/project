from django.urls import path

from administracion.views import Index, ViewModulo, AddModulo, EditModulo, DeleteModulo, ViewUsuario, ViewPersona, \
    AddPersona, EditPersona, DeletePersona

app_name = 'administracion'
urlpatterns = [
    path('', Index.as_view(), name="administracion"),
    path('modulo/', ViewModulo.as_view(), name="view_modulo"),
    path('modulo/add', AddModulo.as_view(), name="add_modulo"),
    path('modulo/edit/<int:pk>', EditModulo.as_view(), name="edit_modulo"),
    path('modulo/delete/<int:pk>', DeleteModulo.as_view(), name="delete_modulo"),
    path('usuario/', ViewUsuario.as_view(), name="view_usuario"),
    path('persona/', ViewPersona.as_view(), name="view_persona"),
    path('persona/add', AddPersona.as_view(), name="add_persona"),
    path('persona/edit/<int:pk>', EditPersona.as_view(), name="edit_persona"),
    path('persona/delete/<int:pk>', DeletePersona.as_view(), name="delete_persona"),
    # path('empresa/', ViewEmpresa.as_view(), name="view_empresa"),
    # path('empresa/add', AddEmpresa.as_view(), name="add_empresa"),
    # path('empresa/edit/<int:pk>', EditEmpresa.as_view(), name="edit_empresa"),
    # path('empresa/delete/<int:pk>', DeleteEmpresa.as_view(), name="delete_empresa"),

]
