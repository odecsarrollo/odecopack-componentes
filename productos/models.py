from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from proveedores.models import MargenProvedor
from model_utils.models import TimeStampedModel
from productos_categorias.models import CategoriaProducto, CategoriaDosCategoria, TipoProductoCategoría
from productos_caracteristicas.models import (
    ColorProducto,
    MaterialProducto,
    SerieProducto,
    FabricanteProducto,
    UnidadMedida
)
from biable.models import ItemsBiable
from .managers import ArticuloCatalogoActivosQuerySet, ProductoQuerySet


# region Productos
def productos_upload_to(instance, filename):
    basename, file_extention = filename.split(".")
    new_filename = "produ_perfil_%s.%s" % (basename, file_extention)
    return "%s/%s/%s" % ("productos", "foto_perfil", new_filename)


class Producto(TimeStampedModel):
    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 1.0
        if filesize > megabyte_limit * 1024 * 1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

    cg_uno = models.ForeignKey(ItemsBiable, null=True, blank=True, related_name='mis_componentes_bandas',
                               verbose_name='producto cguno')
    referencia = models.CharField(max_length=120, unique=True)
    descripcion_estandar = models.CharField(max_length=200, default='AUTOMATICO')
    descripcion_comercial = models.CharField(max_length=200, default='AUTOMATICO')
    con_nombre_automatico = models.BooleanField(default=True, verbose_name='nombre automático')
    fabricante = models.ForeignKey(FabricanteProducto, verbose_name='fabricante', related_name='mis_productos',
                                   on_delete=models.PROTECT)
    serie = models.ForeignKey(SerieProducto, verbose_name='serie', related_name='mis_productos',
                              on_delete=models.PROTECT, null=True, blank=True)

    # region Caracteristica Físicas Producto
    categoria_dos_por_categoria = models.ForeignKey(
        CategoriaDosCategoria,
        verbose_name='categoría dos',
        on_delete=models.PROTECT,
        related_name='mis_productos'
    )
    tipo_por_categoria = models.ForeignKey(
        TipoProductoCategoría,
        verbose_name='tipo',
        on_delete=models.PROTECT,
        related_name='mis_productos',
        null=True, blank=True
    )
    material = models.ForeignKey(MaterialProducto, verbose_name='material', related_name='mis_productos',
                                 on_delete=models.PROTECT, null=True, blank=True)
    color = models.ForeignKey(ColorProducto, verbose_name='color', related_name='mis_productos',
                              on_delete=models.PROTECT, null=True, blank=True)
    ancho = models.CharField(max_length=120, verbose_name='ancho (mm)', default='N.A')
    alto = models.CharField(max_length=120, verbose_name='alto (mm)', default='N.A')
    longitud = models.CharField(max_length=120, verbose_name='longitud (mt)', default='N.A')
    diametro = models.CharField(max_length=120, verbose_name='diametro (mm)', default='N.A')
    # endregion

    cantidad_empaque = models.DecimalField(max_digits=18, decimal_places=4, default=0)
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.PROTECT, null=True)
    cantidad_minima_venta = models.DecimalField(max_digits=18, decimal_places=4, default=0)

    margen = models.ForeignKey(MargenProvedor, null=True, blank=True, related_name="productos_con_margen",
                               verbose_name="Id MxC")
    costo = models.DecimalField(max_digits=18, decimal_places=4, default=0)
    costo_cop = models.DecimalField(max_digits=18, decimal_places=4, default=0)
    precio_base = models.DecimalField(max_digits=18, decimal_places=4, default=0)
    rentabilidad = models.DecimalField(max_digits=18, decimal_places=4, default=0)

    activo = models.BooleanField(default=True)
    activo_componentes = models.BooleanField(default=False, verbose_name="En Compo.")
    activo_proyectos = models.BooleanField(default=False, verbose_name="En Proy.")
    activo_catalogo = models.BooleanField(default=False, verbose_name="En Cata.")
    activo_ensamble = models.BooleanField(default=False, verbose_name="Para Ensam.")

    foto_perfil = models.ImageField(upload_to=productos_upload_to, validators=[validate_image], null=True, blank=True)
    created_by = models.ForeignKey(User, editable=False, null=True, blank=True, related_name="servicio_created")
    updated_by = models.ForeignKey(User, editable=False, null=True, blank=True, related_name="servicio_updated")

    objects = models.Manager()
    activos = ProductoQuerySet.as_manager()

    class Meta:
        verbose_name_plural = "Componentes Bandas"
        verbose_name = "Componente Banda"
        unique_together = ('referencia', 'fabricante')

    def get_costo_cop(self):
        if self.margen:
            return round(self.margen.proveedor.moneda.cambio * self.margen.proveedor.factor_importacion * self.costo, 0)
        return 0

    def get_costo_cop_aereo(self):
        if self.margen:
            if self.margen.proveedor.factor_importacion_aereo > self.margen.proveedor.factor_importacion:
                return round(
                    self.margen.proveedor.moneda.cambio * self.margen.proveedor.factor_importacion_aereo * self.costo,
                    0)
        return 0

    def get_precio_base(self):
        if self.margen:
            return round(self.get_costo_cop() / (1 - (self.margen.margen_deseado / 100)), 0)
        return 0

    def get_precio_base_aereo(self):
        if self.margen:
            return round(self.get_costo_cop_aereo() / (1 - (self.margen.margen_deseado / 100)), 0)
        return 0

    def get_rentabilidad(self):
        if self.margen:
            return round(self.get_precio_base() - self.get_costo_cop(), 0)
        return 0

    def __str__(self):
        return "%s" % (self.descripcion_comercial)

    def get_nombre_automatico(self, tipo):
        if self.con_nombre_automatico:
            nombre = ''
            configuracion = self.categoria_dos_por_categoria.categoria_uno.mi_configuracion_producto_nombre_estandar
            if configuracion.con_categoría_uno:

                if tipo == 'comercial':
                    nombre += ' %s' % self.categoria_dos_por_categoria.categoria_uno.nombre
                if tipo == 'estandar':
                    nombre += ' %s' % self.categoria_dos_por_categoria.categoria_uno.nomenclatura

            if configuracion.con_categoría_dos:
                if tipo == 'comercial':
                    nombre += ' %s' % self.categoria_dos_por_categoria.categoria_dos.nombre
                if tipo == 'estandar':
                    nombre += ' %s' % self.categoria_dos_por_categoria.categoria_dos.nomenclatura

            if tipo == 'estandar':
                if configuracion.con_fabricante:
                    nombre += ' %s' % self.fabricante.nomenclatura

            if configuracion.con_tipo and self.tipo_por_categoria:
                if tipo == 'comercial':
                    nombre += ' %s' % self.tipo_por_categoria.tipo.nombre
                if tipo == 'estandar':
                    nombre += ' %s' % self.tipo_por_categoria.tipo.nomenclatura

            if configuracion.con_material and self.material:

                if tipo == 'comercial':
                    nombre += ' %s' % self.material.nombre
                if tipo == 'estandar':
                    nombre += ' %s' % self.material.nomenclatura

            if configuracion.con_color and self.color:
                if tipo == 'comercial':
                    nombre += ' %s' % self.color.nombre
                if tipo == 'estandar':
                    nombre += ' %s' % self.color.nomenclatura

            if configuracion.con_serie and self.serie:
                if tipo == 'comercial':
                    nombre += ' %s' % self.serie.nombre
                if tipo == 'estandar':
                    nombre += ' %s' % self.serie.nomenclatura

            if configuracion.con_ancho and self.ancho != 'N.A':
                nombre += ' W%s' % self.ancho

            if configuracion.con_alto and self.alto != 'N.A':
                nombre += ' H%s' % self.alto

            if configuracion.con_longitud and self.longitud != 'N.A':
                nombre += ' L%s' % self.longitud

            if configuracion.con_diametro and self.diametro != 'N.A':
                nombre += ' D%s' % self.diametro

            if tipo == 'comercial':
                self.descripcion_comercial = nombre.strip().title()

            if tipo == 'estandar':
                self.descripcion_estandar = nombre.strip().upper()


# endregion


class ArticuloCatalogo(models.Model):
    cg_uno = models.ForeignKey(ItemsBiable, null=True, blank=True, related_name='mis_articulos_catalogo',
                               verbose_name='producto cguno')
    referencia = models.CharField(max_length=100)
    nombre = models.CharField(max_length=200)
    unidad_medida = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100, null=True, blank=True)
    costo = models.DecimalField(max_digits=18, decimal_places=4, default=0)
    fabricante = models.ForeignKey(
        FabricanteProducto,
        verbose_name='fabricante',
        related_name='mis_articulos_catalogo',
        on_delete=models.PROTECT,
        null=True, blank=True
    )
    margen = models.ForeignKey(MargenProvedor, null=True, blank=True, related_name="articulos_catalogo_con_margen",
                               verbose_name="Id MxC")

    activo = models.BooleanField(default=True)
    origen = models.CharField(max_length=20, default='LP_INTRANET')

    activos = ArticuloCatalogoActivosQuerySet.as_manager()

    class Meta:
        unique_together = ('referencia', 'fabricante', 'origen')

    def __str__(self):
        return self.nombre

    def get_costo_cop(self):
        if self.margen:
            return round(self.margen.proveedor.moneda.cambio * self.margen.proveedor.factor_importacion * self.costo, 0)
        return 0

    def get_costo_cop_aereo(self):
        if self.margen:
            return round(
                self.margen.proveedor.moneda.cambio * self.margen.proveedor.factor_importacion_aereo * self.costo, 0)
        return 0

    def get_precio_base(self):
        if self.margen:
            return round(self.get_costo_cop() / (1 - (self.margen.margen_deseado / 100)), 0)
        return 0

    def get_precio_base_aereo(self):
        if self.margen:
            if self.margen.proveedor.factor_importacion_aereo > self.margen.proveedor.factor_importacion:
                return round(self.get_costo_cop_aereo() / (1 - (self.margen.margen_deseado / 100)), 0)
        return 0

    def get_rentabilidad(self):
        if self.margen:
            return round(self.get_precio_base() - self.get_costo_cop(), 0)
        return 0
