from django.db import models

# Create your models here.
from django.urls import reverse_lazy, reverse

from inventario.models import ModeloBase


class Modulo(ModeloBase):
    nombre = models.CharField(verbose_name="Nombre", unique=True, max_length=200)
    descripcion = models.CharField(verbose_name="Descripción", unique=True, max_length=200)
    name_tag = models.CharField(verbose_name="name tag", unique=True, max_length=200)
    activo = models.BooleanField(verbose_name="¿Módulo activo?")

    class Meta:
        verbose_name = "Módulo del sistema"
        verbose_name_plural = "Módulos del sistema"
        ordering = ['-id']

    def __str__(self):
        return u'%s' % self.nombre

    def url(self):
        return reverse(self.name_tag.__str__())

