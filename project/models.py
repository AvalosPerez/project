from django.db import models

class ModeloBase(models.Model):

    usuario_creacion = models.ForeignKey('inventario.Usuario', verbose_name='Usuario Creación', blank=True, null=True,
                                         on_delete=models.CASCADE, related_name='+', editable=False)
    fecha_creacion = models.DateTimeField(verbose_name='Fecha creación', auto_now_add=True)
    fecha_modificacion = models.DateTimeField(verbose_name='Fecha Modificación', auto_now=True)
    usuario_modificacion = models.ForeignKey('inventario.Usuario', verbose_name='Usuario Modificación', blank=True, null=True,
                                             on_delete=models.CASCADE, related_name='+', editable=False)
    status = models.BooleanField(verbose_name="Estado del registro", default=True)

    class Meta:
        abstract = True
