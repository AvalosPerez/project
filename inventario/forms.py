from django import forms
from inventario.models import Categoria, UnidadMedida, Insumo, Proveedor


class CategoriaForm(forms.ModelForm):

    def __init__(self, *args,**kwargs):
        super(CategoriaForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Categoria
        fields = '__all__'
        exclude=("status",)


class UnidadMedidaForm(forms.ModelForm):

    def __init__(self, *args,**kwargs):
        super(UnidadMedidaForm, self).__init__(*args, **kwargs)

    class Meta:
        model = UnidadMedida
        fields = '__all__'
        exclude=("status",)


class InsumoForm(forms.ModelForm):

    def __init__(self, *args,**kwargs):
        super(InsumoForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Insumo
        fields = '__all__'
        exclude=("status",)

class ProveedorForm(forms.ModelForm):

    def __init__(self, *args,**kwargs):
        super(ProveedorForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Proveedor
        fields = '__all__'
        exclude=("status",)