from django import forms
from django.db.models import fields

from administracion.models import Modulo,Empresa



class ModuloForm(forms.ModelForm):

    def __init__(self, *args,**kwargs):
        super(ModuloForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Modulo
        fields = '__all__'
        exclude=("status",)


class EmpresaForm(forms.ModelForm):

    def __init__(self, *args,**kwargs):
        super(EmpresaForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Empresa
        fields = '__all__'
        exclude=("status",)


