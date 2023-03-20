from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db import transaction

from administracion.models import Modulo, GroupAccess
from inventario.models import Usuario, Persona, Cliente


class ModuloForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ModuloForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Modulo
        fields = '__all__'
        exclude = ("status",)

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
                    'type': 'checkbox',

                }
            ),

        }




class ClienteForm(forms.ModelForm):

    nombres = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'col': 'col-md-12',
            'imputstyle': 'input-style-1'

        })
    )
    apellidos = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'col': 'col-md-12',
            'imputstyle': 'input-style-1'

        })

    )
    cedula = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'col': 'col-md-12',
            'imputstyle': 'input-style-1'

        })
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'col': 'col-md-12',
            'imputstyle': 'input-style-1'

        })
    )

    def save(self, commit=True):
        if self.instance.pk is None:  # solo se ejecuta si es un objeto nuevo
            try:
                with transaction.atomic():
                    cliente = super().save(commit=False)
                    persona = Persona(
                        nombres= self.cleaned_data['nombres'],
                        apellidos =self.cleaned_data['apellidos'],
                        cedula = self.cleaned_data['cedula'],
                        email =self.cleaned_data['email'],
                    )
                    persona.save()

                    persona.crear_usuario_perfil_cliente()
                    cliente.persona = persona
                    if commit:
                        cliente.save()
                    return cliente
            except Exception as ex:
                raise NameError("Error al generar un nuevo cliente",ex)
                transaction.set_rollback(True)

        else:

            try:
                with transaction.atomic():
                    cliente = super().save(commit=False)
                    persona = Persona.objects.get(pk=cliente.persona.pk)
                    persona.nombres = self.cleaned_data['nombres']
                    persona.apellidos = self.cleaned_data['apellidos']
                    # persona.cedula = self.cleaned_data['cedula']
                    # persona.email = self.cleaned_data['email']
                    persona.save()
                    if commit:
                        cliente.save()
                    return cliente
            except Exception as ex:
                raise NameError("Error al editar un  cliente",ex)
                transaction.set_rollback(True)



    def clean_cedula(self):
        cedula = self.cleaned_data['cedula']
        if not self.instance.pk:
            r = Persona.objects.filter(cedula=cedula)
            if r.count():
                raise ValidationError("cédula ya existe.")
        return cedula

    def clean_email(self):
        email = self.cleaned_data['email']
        if not self.instance.pk:
            r = Persona.objects.filter(email=email)
            if r.count():
                raise ValidationError("email ya existe.")
        return email



    class Meta:
        model = Cliente
        fields = ['nombres', 'apellidos', 'cedula', 'email', ]


class UsuarioForm(forms.ModelForm):

    nombres = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'col': 'col-md-12',
            'imputstyle': 'input-style-1'

        })
    )
    apellidos = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'col': 'col-md-12',
            'imputstyle': 'input-style-1'

        })

    )
    cedula = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'col': 'col-md-12',
            'imputstyle': 'input-style-1'

        })
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'col': 'col-md-12',
            'imputstyle': 'input-style-1'

        })
    )

    def save(self, commit=True):
        if self.instance.pk is None:  # solo se ejecuta si es un objeto nuevo
            try:
                with transaction.atomic():
                    usuario = super().save(commit=False)


                    persona = Persona(
                        nombres= self.cleaned_data['nombres'],
                        apellidos =self.cleaned_data['apellidos'],
                        cedula = self.cleaned_data['cedula'],
                        email =self.cleaned_data['email'],
                    )
                    persona.save()
                    if commit:
                        usuario.save()
                    persona.usuario = usuario
                    persona.save()
                    usuario.email =persona.email
                    usuario.set_password(persona.cedula)
                    usuario.save()
                    grupo = Group.objects.get(name='Administrador')
                    usuario.groups.add(grupo)
                    return usuario
            except Exception as ex:
                 raise NameError("Error al generar un nuevo usuario",ex)
                 transaction.set_rollback(True)

        else:

            try:
                with transaction.atomic():
                    usuario = super().save(commit=False)
                    persona = Persona.objects.get(usuario=usuario)
                    persona.nombres = self.cleaned_data['nombres']
                    persona.apellidos = self.cleaned_data['apellidos']
                    # persona.cedula = self.cleaned_data['cedula']
                    # persona.email = self.cleaned_data['email']
                    persona.save()
                    if commit:
                        usuario.save()
                    return usuario
            except Exception as ex:
                raise NameError("Error al editar un  usuario",ex)
                transaction.set_rollback(True)



    def clean_cedula(self):
        cedula = self.cleaned_data['cedula']
        if not self.instance.pk:
            r = Persona.objects.filter(cedula=cedula)
            if r.count():
                raise ValidationError("cédula ya existe.")
        return cedula

    def clean_email(self):
        email = self.cleaned_data['email']
        if not self.instance.pk:
            r = Persona.objects.filter(email=email)
            if r.count():
                raise ValidationError("email ya existe.")
        return email



    class Meta:
        model = Usuario
        fields = ['nombres', 'apellidos', 'cedula', 'email', ]



class GroupAccessForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GroupAccessForm, self).__init__(*args, **kwargs)
        if self.instance.pk is None:  # solo se ejecuta si es un objeto nuevo
            grupos = self.fields['grupos']
            grupos.queryset = Group.objects.all().exclude(
                pk__in=GroupAccess.objects.values_list('grupos_id', flat=True).filter(status=True))

    class Meta:
        model = GroupAccess
        fields = '__all__'
        exclude = ("status",)
        widgets = {
            'grupos': forms.Select(

                attrs={
                    'class': 'form-control',
                    'col': 'col-md-12',
                    'imputstyle': 'select-style-1'

                }
            ),
            'modulos': forms.CheckboxSelectMultiple(
                attrs={

                    'col': 'col-md-12',

                }
            ),

        }
