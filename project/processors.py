from administracion.models import Modulo, GroupAccess


def context_dict(request):
    context = {}
    mis_grupos = request.user.groups.all()
    id_acceso_modulo = GroupAccess.objects.values_list('modulos',flat=True).filter(status=True,grupos__in= mis_grupos).distinct()
    context['mis_modulo']= Modulo.objects.filter(status=True, activo=True,pk__in=id_acceso_modulo)
    return context
