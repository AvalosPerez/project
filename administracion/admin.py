from django.contrib import admin

# Register your models here.
from administracion.models import Modulo
from inventario.models import Categoria, UnidadMedida, Proveedor, Insumo, Usuario, Persona, Cliente

admin.site.register(Categoria)
admin.site.register(UnidadMedida)
admin.site.register(Proveedor)
admin.site.register(Insumo)
admin.site.register(Modulo)
admin.site.register(Usuario)
admin.site.register(Persona)
admin.site.register(Cliente)

