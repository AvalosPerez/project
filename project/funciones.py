# Create your models here.
from django.db import models


class ModeloBase(models.Model):
    from django.contrib.auth.models import User
    usuario_creacion = models.ForeignKey(User, verbose_name='Usuario Creación', blank=True, null=True,
                                         on_delete=models.CASCADE, related_name='+', editable=False)
    fecha_creacion = models.DateTimeField(verbose_name='Fecha creación', auto_now_add=True)
    fecha_modificacion = models.DateTimeField(verbose_name='Fecha Modificación', auto_now=True)
    usuario_modificacion = models.ForeignKey(User, verbose_name='Usuario Modificación', blank=True, null=True,
                                             on_delete=models.CASCADE, related_name='+', editable=False)
    status = models.BooleanField(verbose_name="Estado del registro", default=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        usuario = None
        if len(args):
            usuario = args[0].user.id
        if self.id:
            self.usuario_modificacion_id = usuario
        else:
            self.usuario_creacion_id = usuario
        models.Model.save(self)
