from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import fields

from administracion.models import Modulo
from inventario.models import Usuario, Persona


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

            'icon_class': forms.TextInput(
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


class UsuarioForm(UserCreationForm):


    class Meta:
        model = Usuario
        fields = ('email', 'password1', 'password2','is_staff','is_superuser','is_active')

        widgets = {

            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-12',
                    'imputstyle': 'input-style-1'

                }
            ),

            'is_staff': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                    'col': 'col-md-4',
                    'imputstyle': 'form-check form-switch toggle-switch'

                }
            ),
            'is_active': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                    'col': 'col-md-4',
                    'imputstyle': 'form-check form-switch toggle-switch'

                }
            ),

            'is_superuser': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                    'col': 'col-md-4',
                    'imputstyle': 'form-check form-switch toggle-switch'

                }
            ),

            'password': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-12',
                    'imputstyle': 'input-style-1'

                }
            ),

        }


    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class PersonaForm(forms.ModelForm):

    def save(self, commit=True):
        if self.instance.pk is None:  # solo se ejecuta si es un objeto nuevo
            try:
                persona= super().save(commit=False)
                persona.crear_usuario()
                if commit:
                    persona.save()
                return persona
            except Exception as ex:
                raise NameError("Error al generar el nombre de usuario")
                return None
        else:
            return super().save(commit=commit)

    class Meta:
        model = Persona
        fields = '__all__'
        exclude = ('status','usuario',)

        widgets = {
            'nombres': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-12',
                    'imputstyle': 'input-style-1'

                }
            ),

            'apellidos': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-12',
                    'imputstyle': 'input-style-1'

                }
            ),

            'cedula': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-12',
                    'imputstyle': 'input-style-1'

                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-12',
                    'imputstyle': 'input-style-1'

                }
            ),

        }



#
# class EmpresaForm(forms.ModelForm):
#
#     def __init__(self, *args,**kwargs):
#         super(EmpresaForm, self).__init__(*args, **kwargs)

    #
    # class Meta:
    #     model = Empresa
    #     fields = '__all__'
    #     exclude=("status",)
    #
    #     widgets = {
    #         'nombre': forms.TextInput(
    #             attrs={
    #                 'class': 'form-control',
    #                 'col': 'col-md-12',
    #                 'imputstyle': 'input-style-1'
    #
    #             }
    #         ),
    #
    #     }
    #
    #
