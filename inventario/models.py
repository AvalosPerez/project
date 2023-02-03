from django.contrib.auth.models import User
from django.db import models

TIPO_MOVIMIENTO = (
    (1, u"Inicial"),
    (2, u"Entrada"),
    (3, u"Salida"),
)

TIPO_METODO = (
    (1, u"Promedio ponderado"),
)


# Create your models here.
class ModeloBase(models.Model):
    from django.contrib.auth.models import User
    usuario_creacion = models.ForeignKey(User, verbose_name='Usuario Creación', blank=True, null=True,
                                         on_delete=models.CASCADE, related_name='+', editable=False)
    fecha_creacion = models.DateTimeField(verbose_name='Fecha creación', auto_now_add=True)
    fecha_modificacion = models.DateTimeField(verbose_name='Fecha Modificación', auto_now=True)
    usuario_modificacion = models.ForeignKey(User, verbose_name='Usuario Modificación', blank=True, null=True,
                                             on_delete=models.CASCADE, related_name='+', editable=False)
    status = models.BooleanField(verbose_name="Estado del registro", default=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        usuario = None
        if len(args):
            usuario = args[0].user.id
        if self.id:
            self.usuario_modificacion_id = usuario
        else:
            self.usuario_creacion_id = usuario
        models.Model.save(self)


class Empresa(ModeloBase):
    nombre = models.CharField(verbose_name="Empresa", max_length=240)

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresa"
        ordering = ['-id']

    def __str__(self):
        return f'{self.nombre}'


class Persona(ModeloBase):
    usuario = models.OneToOneField(User, verbose_name="Usuario", blank=True, null=True, on_delete=models.CASCADE)
    nombres = models.CharField(verbose_name="Nombres", max_length=450)
    apellidos = models.CharField(verbose_name="Nombres", max_length=450)
    email = models.EmailField(verbose_name="Email", unique=True)
    cedula = models.CharField(verbose_name="Cédula", max_length=10, unique=True)

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
        ordering = ['-id']

    def __str__(self):
        return f'{self.apellidos} {self.nombres}'


class Cliente(ModeloBase):
    persona = models.ForeignKey(Persona, verbose_name="Persona", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['-id']

    def __str__(self):
        return f"{self.persona}"


class Empleado(ModeloBase):
    persona = models.ForeignKey(Persona, verbose_name="Empleado", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        ordering = ['-id']

    def __str__(self):
        return f"{self.persona}"


class Categoria(ModeloBase):
    descripcion = models.CharField(verbose_name="Categoria", unique=True, max_length=200)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['-id']

    def __str__(self):
        return f'{self.descripcion}'


class UnidadMedida(ModeloBase):
    descripcion = models.CharField(verbose_name="Unidad de medida", unique=True, max_length=200)
    alias = models.CharField(verbose_name="Alias", unique=True, max_length=200)

    class Meta:
        verbose_name = "Unidad de medida"
        verbose_name_plural = "Unidades de medidas"
        ordering = ['-id']

    def __str__(self):
        return f'{self.descripcion}'


class Proveedor(ModeloBase):
    razon_social = models.CharField(verbose_name="Razón social", unique=True, max_length=200)
    email = models.EmailField(verbose_name="Email", unique=True, max_length=200)
    telefono = models.CharField(verbose_name="Telefono", max_length=10)

    def __str__(self):
        return f'{self.razon_social}'

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['-id']


class Insumo(ModeloBase):
    metodo_inventario = models.CharField('Método inventario', choices=TIPO_METODO, default=1, max_length=1)
    categoria = models.ForeignKey(Categoria, verbose_name='Categoría', on_delete=models.CASCADE)
    unidad_medida = models.ForeignKey(UnidadMedida, verbose_name='Unidad de medida', on_delete=models.CASCADE)
    lote = models.CharField(verbose_name="Lote", max_length=10)
    descripcion = models.CharField(verbose_name="Insumo", unique=True, max_length=200)
    presentacion_comercial = models.CharField(verbose_name="Presentacion Comercial", unique=True, max_length=200)
    fecha_vencimiento = models.DateField(verbose_name="Fecha vencimiento")
    minimo = models.IntegerField(verbose_name="Mínimo")
    maximo = models.IntegerField(verbose_name="Máximo")
    proveedor = models.ForeignKey(Proveedor, verbose_name="Proveedor", on_delete=models.CASCADE)
    cantidad = models.IntegerField(verbose_name="Stock", default=0)
    costo_unitario = models.DecimalField(verbose_name="Costo Unitario",max_digits=4, decimal_places=2)
    precio_venta = models.DecimalField(verbose_name="Precio Venta",max_digits=4, decimal_places=2)
    aplica_iva = models.BooleanField(verbose_name="¿Aplica IVA?")

    class Meta:
        verbose_name = "Insumo"
        verbose_name_plural = "Insumos"
        ordering = ['-id']

    def __str__(self):
        return f'{self.descripcion}'


class Kardex(ModeloBase):
    empresa = models.ForeignKey(Empresa, verbose_name="Empresa", on_delete=models.CASCADE)
    insumo = models.ForeignKey(Insumo, verbose_name="Insumo", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Kardex"
        verbose_name_plural = "Kardex"
        ordering = ['-id']

    def __str__(self):
        return f'{self.insumo}'


class DetalleKardex(ModeloBase):
    fecha = models.DateField(verbose_name="Fecha")
    kardex = models.ForeignKey(Kardex, verbose_name="Inventario", on_delete=models.CASCADE)
    tipo_movimiento = models.CharField('Tipo movimiento', choices=TIPO_MOVIMIENTO, default=1, max_length=1)
    detalle = models.CharField(verbose_name="Detalle", max_length=450)
    cantidad = models.IntegerField(verbose_name="Cantidad")
    costo_unitario = models.DecimalField(verbose_name="Costo unitario",max_digits=4 , decimal_places=2)
    importe = models.DecimalField(verbose_name="Importe",max_digits=4, decimal_places=2)
    cantidad_anterior = models.IntegerField(verbose_name="Cantidad Anterior")
    costo_anterior = models.DecimalField(verbose_name="Costo Anterior",max_digits=4, decimal_places=2)
    import_anterior = models.DecimalField(verbose_name="Importe Anterior",max_digits=4, decimal_places=2)

    class Meta:
        verbose_name = "Detalle Kardex"
        verbose_name_plural = "DetalleKardex"
        ordering = ['-id']

    def __str__(self):
        return f'tipo: {self.tipo_movimiento} - producto: {self.kardex}'


class Venta(ModeloBase):
    fecha = models.DateField(verbose_name="Fecha venta")
    cliente = models.ForeignKey(Cliente, verbose_name="Cliente", on_delete=models.CASCADE)
    subtotal = models.DecimalField(verbose_name="Subtotal",max_digits=4, decimal_places=2)
    iva = models.DecimalField(verbose_name="Iva",max_digits=4, decimal_places=2)
    total = models.DecimalField(verbose_name="Total",max_digits=4, decimal_places=2)

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['-id']

    def __str__(self):
        return f'{self.fecha} - {self.cliente}'


class DetalleVenta(ModeloBase):
    venta = models.ForeignKey(Venta, verbose_name="Venta", on_delete=models.CASCADE)
    cantidad = models.IntegerField(verbose_name="Cantidad")
    insumo = models.ForeignKey(Insumo, verbose_name="Venta", on_delete=models.CASCADE)
    importe = models.DecimalField(verbose_name="Total",max_digits=4, decimal_places=2)

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['-id']

    def __str__(self):
        return f'{self.venta} - {self.insumo}'


class Compra(ModeloBase):
    fecha = models.DateField(verbose_name="Fecha Compra")
    proveedor = models.ForeignKey(Cliente, verbose_name="Proveedor", on_delete=models.CASCADE)
    total = models.DecimalField(verbose_name="Total",max_digits=4, decimal_places=2)

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
        ordering = ['-id']

    def __str__(self):
        return f'{self.fecha} - {self.proveedor}'


class DetalleCompra(ModeloBase):
    compra = models.ForeignKey(Compra, verbose_name="Compra", on_delete=models.CASCADE)
    insumo = models.ForeignKey(Insumo, verbose_name="Insumo", on_delete=models.CASCADE)
    cantidad = models.IntegerField(verbose_name="Cantidad")
    costo = models.IntegerField(verbose_name="Cantidad")
    importe = models.DecimalField(verbose_name="Importe",max_digits=4, decimal_places=2)

    class Meta:
        verbose_name = "Detalle Compra"
        verbose_name_plural = "Detalle Compra"
        ordering = ['-id']

    def __str__(self):
        return f'{self.compra} - {self.insumo}'
