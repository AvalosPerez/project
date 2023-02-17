from django import template

from administracion.models import Modulo

register = template.Library()

@register.simple_tag
def get_modulos_list():
    modulos = Modulo.objects.filter(status=True, activo=True)
    return modulos