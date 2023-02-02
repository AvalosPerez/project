from django.db import models


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


class Insumo(ModeloBase):
    categoria = models.ForeignKey(Categoria, verbose_name='Categoría', on_delete=models.CASCADE)
    unidad_medida = models.ForeignKey(UnidadMedida, verbose_name='Unidad de medida', on_delete=models.CASCADE)
    descripcion = models.CharField(verbose_name="Insumo", unique=True, max_length=200)
    minimo = models.IntegerField(verbose_name="Mínimo")
    maximo = models.IntegerField(verbose_name="Máximo")

    class Meta:
        verbose_name = "Insumo"
        verbose_name_plural = "Insumos"
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





