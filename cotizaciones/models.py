import datetime
import random

from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

from bandas.models import Banda
from model_utils.models import TimeStampedModel

from .managers import CotizacionesEstadosQuerySet
from productos.models import Producto, ArticuloCatalogo
from listasprecios.models import FormaPago
from biable.models import FacturasBiable, Cliente as ClienteBiable
from geografia_colombia.models import Ciudad
from contactos.models import ContactoEmpresa


# Create your models here.
# region Cotizaciones
class Cotizacion(TimeStampedModel):
    ESTADOS = (
        ('INI', 'Iniciado'),
        ('ENV', 'Enviada'),
        ('ELI', 'Rechazada'),
        ('REC', 'Recibida'),
        ('PRO', 'En Proceso'),
        ('FIN', 'Entragada Totalmente'),
    )
    estado = models.CharField(max_length=10, choices=ESTADOS, default='INI')
    nro_contacto = models.CharField(null=True, blank=True, max_length=30)  # validators should be a list
    email = models.EmailField(max_length=150)
    nombres_contacto = models.CharField(max_length=120)
    pais = models.CharField(max_length=120, blank=True, null=True)
    ciudad = models.CharField(max_length=120, blank=True, null=True)
    apellidos_contacto = models.CharField(max_length=120)
    razon_social = models.CharField(max_length=120, blank=True, null=True)
    nro_cotizacion = models.CharField(max_length=120)
    fecha_envio = models.DateTimeField(null=True, blank=True)
    total = models.DecimalField(max_digits=18, decimal_places=0, default=0)
    total_venta_perdida = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    usuario = models.ForeignKey(User, related_name='mis_cotizaciones')
    creado_por = models.ForeignKey(User, related_name='cotizaciones_creadas', editable=False)
    observaciones = models.TextField(max_length=300, blank=True, null=True)
    en_edicion = models.BooleanField(default=False)
    version = models.PositiveIntegerField(default=1)
    ciudad_despacho = models.ForeignKey(Ciudad, null=True, blank=True)
    cliente_biable = models.ForeignKey(ClienteBiable, null=True, blank=True, related_name='mis_cotizaciones')
    cliente_nuevo = models.BooleanField(default=False)
    otra_ciudad = models.BooleanField(default=False)
    sucursal_sub_empresa = models.CharField(max_length=120, blank=True, null=True, verbose_name='Empresa o Sucursal')
    actualmente_cotizador = models.BooleanField(default=False, editable=False)
    contacto = models.ForeignKey(ContactoEmpresa, null=True, blank=True, related_name='mis_cotizaciones')
    contacto_nuevo = models.BooleanField(default=False)

    estados = CotizacionesEstadosQuerySet.as_manager()
    objects = models.Manager()

    class Meta:
        permissions = (
            ('full_cotizacion', 'Full Cotizacion'),
            ('gestion_cotizaciones', 'Gestionar Cotizaciones'),
            # ('hacer_cotizacion', 'Hacer Cotización'),
        )

    def get_absolute_url(self):
        return reverse("cotizaciones:detalle_cotizacion", kwargs={"pk": self.pk})

    def update_total(self):
        "updating..."
        total = 0
        descuento = 0
        total_venta_perdida = 0
        items = self.items.all()
        for item in items:
            total += item.total
            descuento += item.descuento
            total_venta_perdida += item.valor_venta_perdida_total
        self.total = total
        self.total_venta_perdida = total_venta_perdida
        self.descuento = descuento
        self.save()

    def set_estado(self, estado):
        self.estado = estado
        self.save()

    def get_rentabilidad_actual_total(self):
        rentabilidad = 0
        for item in self.items.all():
            rentabilidad += item.get_rentabilidad_actual_total()
        return rentabilidad

    def __str__(self):
        return "%s" % self.nro_cotizacion


# endregion

# region ItemCotizacion
class ItemCotizacion(TimeStampedModel):
    cotizacion = models.ForeignKey(Cotizacion, related_name="items")
    cantidad = models.DecimalField(max_digits=18, decimal_places=3, null=True)
    precio = models.DecimalField(max_digits=18, decimal_places=2)
    dias_entrega = models.PositiveIntegerField(default=0)
    forma_pago = models.ForeignKey(FormaPago, related_name="items_cotizaciones", null=True)
    p_n_lista_descripcion = models.CharField(max_length=120, null=True, verbose_name='Descripción Otro')
    p_n_lista_referencia = models.CharField(max_length=120, null=True, verbose_name='Referencia Otro', blank=True)
    p_n_lista_unidad_medida = models.CharField(max_length=120, null=True, verbose_name='Unidad Medida')
    total = models.DecimalField(max_digits=18, decimal_places=2)


    item = models.ForeignKey(Producto, related_name="cotizaciones", null=True)#componentes
    banda = models.ForeignKey(Banda, related_name="cotizaciones", null=True)
    articulo_catalogo = models.ForeignKey(ArticuloCatalogo, related_name="cotizaciones", null=True)#ItemVentaCatalogo


    porcentaje_descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    cantidad_venta_perdida = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    motivo_venta_perdida = models.CharField(max_length=120, default="NA")
    transporte_tipo = models.CharField(max_length=120)
    cantidad_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    valor_venta_perdida_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    def get_nombre_item(self):
        if self.item:
            nombre = self.item.descripcion_comercial
        elif self.articulo_catalogo:
            nombre = self.articulo_catalogo.nombre
        elif self.banda:
            nombre = self.banda.descripcion_comercial
        else:
            nombre = self.p_n_lista_descripcion
        return nombre

    def get_referencia_item(self):
        if self.item:
            nombre = self.item.referencia
        elif self.articulo_catalogo:
            nombre = self.articulo_catalogo.referencia
        elif self.banda:
            nombre = self.banda.referencia
        else:
            nombre = self.p_n_lista_referencia
        return nombre

    def get_unidad_item(self):
        if self.item:
            nombre = self.item.unidad_medida
        elif self.articulo_catalogo:
            nombre = self.articulo_catalogo.unidad_medida
        elif self.banda:
            nombre = "Metro"
        else:
            nombre = self.p_n_lista_unidad_medida
        return nombre

    def get_costo_cop_actual_unidad(self):
        if self.item:
            costo = self.item.get_costo_cop()
        elif self.articulo_catalogo:
            costo = self.articulo_catalogo.get_costo_cop()
        elif self.banda:
            costo = self.banda.get_costo_cop()
        else:
            costo = 0
        return round(costo, 0)

    def get_costo_cop_actual_total(self):
        return round(self.get_costo_cop_actual_unidad() * self.cantidad_total, 0)

    def get_rentabilidad_actual_total(self):
        costo = self.get_costo_cop_actual_total()
        return round(self.total - costo, 0)

    def get_margen_rentabilidad_actual(self):
        margen = 0
        if not self.p_n_lista_descripcion:
            if self.total != 0:
                return round((self.get_rentabilidad_actual_total() * 100) / self.total, 2)
        return margen

    def get_tiempo_entrega_prometido(self):
        if self.dias_entrega == 0:
            return "Inmediato"
        if self.dias_entrega == 1:
            return "%s dia" % self.dias_entrega
        return "%s dias" % self.dias_entrega


# endregion

# region Remisiones
class RemisionCotizacion(TimeStampedModel):
    tipo_remision = models.CharField(max_length=2, choices=(('RM', 'RM'), ('RY', 'RY')), default='RM')
    nro_remision = models.PositiveIntegerField()
    factura_biable = models.ForeignKey(FacturasBiable, null=True, blank=True, related_name='mis_remisiones')
    fecha_prometida_entrega = models.DateField()
    entregado = models.BooleanField(default=False)
    cotizacion = models.ForeignKey(Cotizacion, related_name="mis_remisiones")

    class Meta:
        verbose_name_plural = "Remisiones x Cotización"

    def __str__(self):
        return "%s" % self.nro_remision

    def get_dias_a_fecha_fin(self):
        return (self.fecha_prometida_entrega - datetime.date.today()).days


# endregion

# region Tareas
class TareaCotizacion(TimeStampedModel):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(max_length=300)
    fecha_inicial = models.DateField()
    fecha_final = models.DateField()
    esta_finalizada = models.BooleanField(default=False)
    cotizacion = models.ForeignKey(Cotizacion, null=True, blank=True, related_name="mis_tareas")

    class Meta:
        verbose_name_plural = "Tareas"

    def __str__(self):
        return "%s" % self.nombre

    def get_dias_a_fecha_fin(self):
        return (self.fecha_final - datetime.date.today()).days


class ComentarioCotizacion(TimeStampedModel):
    comentario = models.TextField(max_length=300)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='comentarios_cotizaciones')
    cotizacion = models.ForeignKey(Cotizacion, null=True, blank=True, related_name="mis_comentarios")


def imagen_upload_to(instance, filename):
    fecha_hoy = timezone.now().strftime('%Y%m%d%H%M%S')
    split_filename = filename.split(".")
    file_extention = split_filename[-1]
    basename = split_filename[0]
    new_filename = '%s %s' % (basename, fecha_hoy)
    return "img/coti/%s/%s.%s" % (instance.cotizacion.id, new_filename, file_extention)


class ImagenCotizacion(TimeStampedModel):
    cotizacion = models.ForeignKey(Cotizacion, related_name='mis_imagenes')
    imagen = models.ImageField(upload_to=imagen_upload_to)
    imagen_cotizador = ImageSpecField(source='imagen',
                                      processors=[ResizeToFill(150, 150)],
                                      format='JPEG',
                                      options={'quality': 60})

# endregion
