from django import forms
from django.db import transaction

from inventario.models import Categoria, UnidadMedida, Insumo, Proveedor, Compra, Venta, DetalleVenta


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

    def save(self, commit=True):
        if self.instance.pk is None:  # solo se ejecuta si es un objeto nuevo
            try:
                insumo= super().save(commit=commit)
                insumo.generar_inventario_inicial()
                return insumo
            except Exception as ex:
                raise NameError("Error al generar el inventario inicial")
                return None
        else:
            return super().save(commit=commit)


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
                        'min': '0',
                        'step':'0.01',

                    }
                ),

                'precio_venta': forms.TextInput(
                    attrs={
                        'class': 'form-control',
                        'col': 'col-md-4',
                        'imputstyle': 'input-style-1',
                        'type': 'number',
                        'min': '0',
                        'decimal': '2',
                        'step':'0.01',

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
        exclude = ("status","insumos","total")

        widgets = {
            'fecha': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-6',
                    'imputstyle': 'input-style-1',
                    'type': 'date'

                }
            ),
            'proveedor': forms.Select(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-6',
                    'imputstyle': 'select-style-1'

                }
            ),

        }


class VentaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(VentaForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        if self.instance.pk is None:  # solo se ejecuta si es un objeto nuevo
            try:
                with transaction.atomic():
                    venta= super().save(commit=False)
                    venta.fecha = self.cleaned_data['fecha']
                    venta.cliente = self.cleaned_data['cliente']
                    venta.total = float(self.initial['total'])
                    if commit:
                        venta.save()
                    lista_id_insumos =self.initial['id_insumos']
                    lista_cantidad =self.initial['cantidad']
                    for id_insumo, cant in zip(lista_id_insumos, lista_cantidad):
                        id= int(id_insumo)
                        cantidad= int(cant)
                        insumo= Insumo.objects.get(pk=id)
                        importe = float(cantidad * insumo.precio_venta)
                        detalle_venta = DetalleVenta(venta = venta,insumo=insumo, cantidad=cantidad,importe=importe)
                        detalle_venta.save()
                        detalle_venta.generar_inventario_movimiento_salida(cantidad)
                    return venta

            except Exception as ex:
                raise NameError("Error al guardar la venta")
                return None
        else:
            return super().save(commit=commit)

    class Meta:
        model = Venta
        fields = '__all__'
        exclude = ("status",)

        widgets = {
            'fecha': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-6',
                    'imputstyle': 'input-style-1',
                    'type': 'date'

                }
            ),
            'cliente': forms.Select(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-6',
                    'imputstyle': 'select-style-1'

                }
            ),

            'subtotal': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-6',
                    'imputstyle': 'input-style-1',


                }
            ),
            'total': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'col': 'col-md-6',
                    'imputstyle': 'input-style-1',
                    'id':'id_total_total',
                    'disabled':'True',


                }
            ),




        }
