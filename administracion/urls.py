from django.urls import path

from administracion.views import Index, ViewModulo, EditModulo, DeleteModulo, AddModulo

app_name = 'administracion'
urlpatterns = [
    path('', Index.as_view(), name="administracion"),
    path('modulo/', ViewModulo.as_view(), name="view_modulo"),
    path('modulo/add', AddModulo.as_view(), name="add_modulo"),
    path('modulo/edit/<int:pk>', EditModulo.as_view(), name="edit_modulo"),
    path('modulo/delete/<int:pk>', DeleteModulo.as_view(), name="delete_modulo"),

]
