from django import forms
from inventario.models import Categoria, UnidadMedida, Insumo, Proveedor, Compra


class CategoriaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CategoriaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = ' form-control   form-row '
            visible.field.widget.attrs['fieldset_class'] = ' input-style-1'

    class Meta:
        model = Categoria
        fields = '__all__'
        exclude = ("status",)

        widgets = {
            'descripcion': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-12',
                    'imputstyle': 'input-style-1'

                }
            ),

        }


class UnidadMedidaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UnidadMedidaForm, self).__init__(*args, **kwargs)

    class Meta:
        model = UnidadMedida
        fields = '__all__'
        exclude = ("status",)

        widgets = {
            'descripcion': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-12',
                    'imputstyle': 'input-style-1'

                }
            ),
            'alias': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-12',
                    'imputstyle': 'input-style-1'

                }
            ),
        }


class InsumoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(InsumoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Insumo
        fields = '__all__'
        exclude = ("status",)

        widgets = {
            'categoria': forms.Select(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-4',
                    'imputstyle': 'select-style-1'

                }
            ),
            'unidad_medida': forms.Select(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-4',
                    'imputstyle': 'select-style-1'

                }
            ),

            'proveedor': forms.Select(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-4',
                    'imputstyle': 'select-style-1'

                }
            ),


            'descripcion': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-12',
                    'imputstyle': 'input-style-1'

                }
            ),
            'detalle': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-12',
                    'imputstyle': 'input-style-1'

                }
            ),

            'minimo': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-4',
                    'imputstyle': 'input-style-1',
                    'type': 'number',
                    'min': '0'

                }
            ),

            'maximo': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-4',
                    'imputstyle': 'input-style-1',
                    'type': 'number',
                    'min': '0'

                }
            ),


            'cantidad': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-4',
                    'imputstyle': 'input-style-1',
                    'type': 'number',
                    'min': '0'

                }
            ),

            'costo_unitario': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-4',
                    'imputstyle': 'input-style-1',
                    'type': 'number',
                    'min': '0'

                }
            ),

            'precio_venta': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-4',
                    'imputstyle': 'input-style-1',
                    'type': 'number',
                    'min': '0',
                    'decimal': '2'

                }
            ),

        }


class ProveedorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProveedorForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Proveedor
        fields = '__all__'
        exclude = ("status",)

        widgets = {
            'razon_social': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-12',
                    'imputstyle': 'input-style-1'

                }
            ),

            'email': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-12',
                    'imputstyle': 'input-style-1',
                    'placeholder': 'example@gmail.com'
                }
            ),

            'telefono': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-12',
                    'imputstyle': 'input-style-1',
                    'type': 'tel',
                    'maxlength': '10',
                    'placeholder': '099-9999-9999'

                }
            ),

        }


class CompraForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CompraForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Compra
        fields = '__all__'
        exclude = ("status",)

        widgets = {
            'fecha': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-4',
                    'imputstyle': 'input-style-1',
                    'type': 'date'

                }
            ),
            'proveedor': forms.Select(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-4',
                    'imputstyle': 'select-style-1'

                }
            ),
            'total': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-4',
                    'imputstyle': 'input-style-1',
                    'type': 'number',
                    'min': '0',
                    'decimal': '2'

                }
            ),

            'descripcion': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-12',
                    'rows':'4',
                    'imputstyle': 'input-style-1',


                }
            ),

        }
