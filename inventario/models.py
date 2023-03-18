from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User, PermissionsMixin, Group
from django.core.exceptions import ValidationError
from django.db import models, transaction
from project.models import ModeloBase

TIPO_MOVIMIENTO = (
    (1, u"Inicial"),
    (2, u"Entrada"),
    (3, u"Salida"),
)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="Email")
    is_active = models.BooleanField(default=True, verbose_name="¿Activo?")
    is_staff = models.BooleanField(default=False, verbose_name="¿Gestor?")
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def obtener_grupos(self):
        return self.groups.all()

class Persona(ModeloBase):
    nombres = models.CharField(verbose_name="Nombres", max_length=450)
    apellidos = models.CharField(verbose_name="Apellidos", max_length=450)
    cedula = models.CharField(verbose_name="Cédula", max_length=10, unique=True)
    email = models.EmailField(unique=True, verbose_name="Email", null=True, blank=True)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
        ordering = ['-id']

    def __str__(self):
        return f'{self.apellidos} {self.nombres}'

    def crear_usuario_perfil_cliente(self):
        try:
            with transaction.atomic():
                # Creamos el usuario en la tabla User
                usuario = Usuario.objects.create_user(
                    email=self.email,
                    password=self.cedula
                )
                # Asociamos el usuario a la cliente
                self.usuario = usuario
                self.save()
                grupo = Group.objects.get(name='cliente')
                usuario.groups.add(grupo)



        except Exception as ex:
            raise NameError("Error al generar el usuario",ex)
            transaction.set_rollback(True)


class Perfil(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='fotos_perfil/', blank=True)

    def __str__(self):
        return f'Perfil de {self.usuario.persona.nombre} {self.usuario.persona.apellido}'


class Cliente(ModeloBase):
    persona = models.ForeignKey(Persona, verbose_name="Persona", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['-id']

    def __str__(self):
        return f"{self.persona}"

    def en_uso(self):
        return self.venta_set.filter(status=True).exists()

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

    def en_uso(self):
        return self.insumo_set.filter(status=True).exists()


class UnidadMedida(ModeloBase):
    descripcion = models.CharField(verbose_name="Unidad de medida", unique=True, max_length=200)
    alias = models.CharField(verbose_name="Alias", unique=True, max_length=200)

    class Meta:
        verbose_name = "Unidad de medida"
        verbose_name_plural = "Unidades de medidas"
        ordering = ['-id']

    def __str__(self):
        return f'{self.descripcion}'

    def en_uso(self):
        return self.insumo_set.filter(status=True).exists()


class Proveedor(ModeloBase):
    razon_social = models.CharField(verbose_name="Razón social", unique=True, max_length=200)
    email = models.EmailField(verbose_name="Email", unique=True, max_length=200)
    telefono = models.CharField(verbose_name="Telefono", max_length=10)

    def __str__(self):
        return f'{self.razon_social}'

    def en_uso(self):
        return self.insumo_set.filter(status=True).exists()

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['-id']


class Insumo(ModeloBase):
    categoria = models.ForeignKey(Categoria, verbose_name='Categoría', on_delete=models.CASCADE)
    unidad_medida = models.ForeignKey(UnidadMedida, verbose_name='Unidad de medida', on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, verbose_name="Proveedor", on_delete=models.CASCADE)
    descripcion = models.CharField(verbose_name="Insumo", unique=True, max_length=200)
    detalle = models.CharField(verbose_name="Descripción", null=True, max_length=300)
    minimo = models.PositiveIntegerField(verbose_name="Mínimo")
    maximo = models.PositiveIntegerField(verbose_name="Máximo")
    cantidad = models.PositiveIntegerField(verbose_name="Stock", default=0)
    costo_unitario = models.DecimalField(verbose_name="Costo Unitario", max_digits=30, decimal_places=2)
    precio_venta = models.DecimalField(verbose_name="Precio Venta", max_digits=30, decimal_places=2)

    class Meta:
        verbose_name = "Insumo"
        verbose_name_plural = "Insumos"
        ordering = ['-id']

    def __str__(self):
        return f'{self.descripcion}'

    def generar_inventario_inicial(self):
        try:
            with transaction.atomic():
                kardex = Kardex(

                    insumo=self
                )
                kardex.save()
                detalleKardex = DetalleKardex(
                    fecha=datetime.now(),
                    kardex=kardex,
                    tipo_movimiento=1,
                    detalle="Inicial",
                    cantidad=self.cantidad,
                    costo_unitario=self.costo_unitario,
                    importe=(self.cantidad * self.costo_unitario),
                    cantidad_anterior=self.cantidad,
                    costo_anterior=self.costo_unitario,
                    import_anterior=(self.cantidad * self.costo_unitario)
                )
            detalleKardex.save()
        except Exception as ex:
            raise NameError("Error al generar el inventario inicial")
            transaction.set_rollback(True)




class Kardex(ModeloBase):
    insumo = models.ForeignKey(Insumo, verbose_name="Insumo", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Kardex"
        verbose_name_plural = "Kardex"
        ordering = ['-id']

    def __str__(self):
        return f'{self.insumo}'

    def get_existencia(self):
        existencia = self.detallekardex_set.filter(status=True).order_by('-id')[0]
        return existencia.kardex.insumo.cantidad

    def get_costo_existencia(self):
        return self.detallekardex_set.filter(status=True).order_by('-id')[0].costo_anterior

    def get_total_existencia(self):
        return self.detallekardex_set.filter(status=True).order_by('-id')[0].import_anterior

    def get_cantidad_movimiento(self):
        return self.detallekardex_set.filter(status=True).order_by('-id')[0].cantidad

    def get_costo_movimiento(self):
        return self.detallekardex_set.filter(status=True).order_by('-id')[0].costo_unitario

    def get_total_movimiento(self):
        return self.detallekardex_set.filter(status=True).order_by('-id')[0].importe

    def get_inventario_entradas(self):
        entradas = self.detallekardex_set.filter(status=True, tipo_movimiento=2)
        return entradas.count()

    def get_inventario_salidas(self):
        salidas = self.detallekardex_set.filter(status=True, tipo_movimiento=3)
        return salidas.count()

class DetalleKardex(ModeloBase):
    fecha = models.DateField(verbose_name="Fecha")
    kardex = models.ForeignKey(Kardex, verbose_name="Inventario", on_delete=models.CASCADE)
    tipo_movimiento = models.CharField('Tipo movimiento', choices=TIPO_MOVIMIENTO, default=1, max_length=1)
    detalle = models.CharField(verbose_name="Detalle", max_length=450)
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad", default=0)
    costo_unitario = models.DecimalField(verbose_name="Costo unitario", max_digits=30, decimal_places=4, default=0,
                                         null=True)
    importe = models.DecimalField(verbose_name="Importe", max_digits=30, decimal_places=2, default=0)
    cantidad_anterior = models.PositiveIntegerField(verbose_name="Cantidad Anterior", default=0)
    costo_anterior = models.DecimalField(verbose_name="Costo Anterior", max_digits=30, decimal_places=4, default=0)
    import_anterior = models.DecimalField(verbose_name="Importe Anterior", max_digits=30, decimal_places=4, default=0)

    class Meta:
        verbose_name = "Detalle Kardex"
        verbose_name_plural = "DetalleKardex"
        ordering = ['-id']

    def __str__(self):
        return f'tipo: {self.tipo_movimiento} - producto: {self.kardex}'

class Venta(ModeloBase):
    fecha = models.DateField(verbose_name="Fecha venta")
    cliente = models.ForeignKey(Cliente, verbose_name="Cliente", on_delete=models.CASCADE)
    total = models.DecimalField(verbose_name="Total", max_digits=30, decimal_places=2,blank=True)

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['-id']

    def __str__(self):
        return f'{self.fecha} - {self.cliente}'

class DetalleVenta(ModeloBase):
    venta = models.ForeignKey(Venta, verbose_name="Venta", on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")
    insumo = models.ForeignKey(Insumo, verbose_name="Venta", on_delete=models.CASCADE)
    importe = models.DecimalField(verbose_name="Total", max_digits=30, decimal_places=2)

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['-id']

    def __str__(self):
        return f'{self.venta} - {self.insumo}'

    def generar_inventario_movimiento_salida(self,cantidad):
        try:
            with transaction.atomic():
                kardex = Kardex.objects.filter(status=True, insumo=self.insumo).first()
                detalleKardex = DetalleKardex(
                    fecha=datetime.now(),
                    kardex=kardex,
                    tipo_movimiento=3,
                    detalle="Movimiento salida",
                    cantidad=self.cantidad,
                    costo_unitario = self.insumo.precio_venta,
                    importe=(self.cantidad * self.insumo.precio_venta),
                    cantidad_anterior=self.insumo.cantidad,
                    costo_anterior=self.insumo.costo_unitario,
                    import_anterior=((self.insumo.cantidad - self.cantidad) * self.insumo.costo_unitario)
                )
            detalleKardex.save()
            insumo = Insumo.objects.get(pk=self.insumo.pk)
            insumo.cantidad = insumo.cantidad - detalleKardex.cantidad
            insumo.save()
        except Exception as ex:
            raise NameError("Error al generar el inventario salida")
            transaction.set_rollback(True)

class Compra(ModeloBase):
    fecha = models.DateField(verbose_name="Fecha Compra")
    proveedor = models.ForeignKey(Proveedor, verbose_name="Proveedor", on_delete=models.CASCADE)
    total = models.DecimalField(verbose_name="Total", max_digits=30, decimal_places=2)

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
        ordering = ['-id']

    def __str__(self):
        return f'{self.fecha} - {self.proveedor}'


class CompraInsumo(ModeloBase):
    compra = models.ForeignKey(Compra, verbose_name="Compra", on_delete=models.CASCADE)
    insumo = models.ForeignKey(Insumo, verbose_name="Insumo", on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")
    costo = models.DecimalField(verbose_name="Costo",max_digits=30, decimal_places=2)
    importe = models.DecimalField(verbose_name="Importe", max_digits=30, decimal_places=2)

    class Meta:
        verbose_name = "Detalle Compra"
        verbose_name_plural = "Detalle Compra"
        ordering = ['-id']

    def __str__(self):
        return f'{self.compra} - {self.insumo}'
