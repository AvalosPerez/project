from django.contrib.auth.models import Group
from django.db import models

# Create your models here.
from django.urls import reverse_lazy, reverse

from project.models import ModeloBase

class Modulo(ModeloBase):
    nombre = models.CharField(verbose_name="Nombre", unique=True, max_length=200)
    descripcion = models.CharField(verbose_name="Descripción", unique=True, max_length=200)
    name_tag = models.CharField(verbose_name="name tag", unique=True, max_length=200)
    activo = models.BooleanField(verbose_name="¿Módulo activo?")
    icon_class = models.CharField(verbose_name="icon class",default='lni lni-folder', max_length=200)
    class Meta:
        verbose_name = "Módulo del sistema"
        verbose_name_plural = "Módulos del sistema"
        ordering = ['-id']

    def __str__(self):
        return u'%s' % self.nombre

    def url(self):
        try:
            url= reverse(self.name_tag.__str__())
        except Exception:
            url="Javascript:void(0)"
        return url

class GroupAccess(ModeloBase):
    grupos = models.ForeignKey(Group, on_delete=models.CASCADE, help_text="Si el grupo no se encuentra listado en el combo es por que ya fue agregado.")
    modulos = models.ManyToManyField(Modulo)

    def __str__(self):
        return self.grupos.name