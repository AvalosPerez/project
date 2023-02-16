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

        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-12',
                    'imputstyle': 'input-style-1'

                }
            ),
            'descripcion': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-12',
                    'imputstyle': 'input-style-1'

                }
            ),

             'name_tag': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-12',
                    'imputstyle': 'input-style-1'

                }
            ),

             'activo': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                    'col': 'col-md-12',
                    'imputstyle': 'form-check form-switch toggle-switch',
                    'type':'checkbox',

                }
            ),

        }


class EmpresaForm(forms.ModelForm):

    def __init__(self, *args,**kwargs):
        super(EmpresaForm, self).__init__(*args, **kwargs)


    class Meta:
        model = Empresa
        fields = '__all__'
        exclude=("status",)

        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-12',
                    'imputstyle': 'input-style-1'

                }
            ),

        }


