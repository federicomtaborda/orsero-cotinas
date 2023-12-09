from datetime import datetime, time

from django.db import models
from django.db.models import Sum, F, FloatField
from django.db.models.functions import Coalesce
from django.forms import model_to_dict

from config import settings
from core.pos.choices import genders


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Descripción', unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')
    image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    costo_m2 = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, verbose_name='Costo M2')
    costo_colocacion = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, verbose_name='Costo '
                                                                                                       'Colocación')
    costo_flete= models.DecimalField(default=0.00, max_digits=10, decimal_places=2,verbose_name='Costo Flete')
    otros_costos = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, verbose_name='Otros Costos')
    costo_total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, verbose_name='Costo Total')
    ganancia_estimada = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, verbose_name='Ganancia '
                                                                                                      'Estimada')
    tiempo_colocacion = models.TimeField(default=time(0, 0), verbose_name='Tiempo de Colocación')
    precio_venta = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, verbose_name='Precio de Venta')

    def __str__(self):
        return f'{self.name} ({self.category.name})'

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.__str__()
        item['category'] = self.category.toJSON()
        item['image'] = self.get_image()
        return item

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/empty.png'

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']


class Client(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombres')
    direccion_postal = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección Postal')
    direccion_de_trabajo = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección de Trabajo')
    telefono_celular = models.CharField(max_length=150, null=True, blank=True, verbose_name='Tel Celular')
    otro_telefono = models.CharField(max_length=150, null=True, blank=True, verbose_name='Otro Teléfono')
    email = models.CharField(max_length=100, null=True, blank=True, verbose_name='Correo Electrónico')
    observaciones_cliente = models.CharField(max_length=200, null=True, blank=True, verbose_name='Observaciones del cliente')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.names}'

    def toJSON(self):
        item = model_to_dict(self)
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['birthdate'] = self.birthdate.strftime('%Y-%m-%d')
        item['full_name'] = self.get_full_name()
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']


class Company(models.Model):
    name = models.CharField(max_length=150, verbose_name='Razón Social')
    cbu = models.CharField(max_length=25, null=True, blank=True, verbose_name='Cbu')
    alias = models.CharField(max_length=50, null=True, blank=True, verbose_name='Alias')
    cuenta_bancaria = models.CharField(max_length=50, null=True, blank=True, verbose_name='Cuenta Bancaria')
    direccion = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    telefono = models.CharField(max_length=20, null=True, blank=True, verbose_name='Teléfono')
    otro_telefono = models.CharField(max_length=20, null=True, blank=True, verbose_name='Otro Teléfono')
    website = models.CharField(max_length=100, null=True, blank=True, verbose_name='Website')
    image = models.ImageField(upload_to='company/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    observaciones = models.CharField(max_length=150, null=True, blank=True, verbose_name='Observación')

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/empty.png'

    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        return item

    class Meta:
        verbose_name = 'Compañia'
        verbose_name_plural = 'Compañias'
        default_permissions = ()
        permissions = (
            ('change_company', 'Can change Company'),
        )
        ordering = ['id']


class OrdenDeTrabajo(models.Model):
    numero_orden = models.CharField(u'N° Orden de Trabajo', max_length=10, default='')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    ganancia_total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

    def __str__(self):
        return self.client.names

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if Company.objects.all().exists():
            self.company = Company.objects.first()
        super(Sale, self).save()

    def get_number(self):
        return f'{self.id:06d}'

    def toJSON(self):
        item = model_to_dict(self)
        item['number'] = self.get_number()
        item['client'] = self.client.toJSON()
        item['subtotal'] = f'{self.subtotal:.2f}'
        item['iva'] = f'{self.iva:.2f}'
        item['total_iva'] = f'{self.total_iva:.2f}'
        item['total'] = f'{self.total:.2f}'
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['saleproduct'] = [i.toJSON() for i in self.saleproduct_set.all()]
        return item

    def delete(self, using=None, keep_parents=False):
        for detail in self.saleproduct_set.filter(product__is_inventoried=True):
            detail.product.stock += detail.cant
            detail.product.save()
        super(Sale, self).delete()

    def calculate_invoice(self):
        subtotal = self.saleproduct_set.all().aggregate(result=Coalesce(Sum(F('price') * F('cant')), 0.00, output_field=FloatField())).get('result')
        self.subtotal = subtotal
        self.total_iva = self.subtotal * float(self.iva)
        self.total = float(self.subtotal) + float(self.total_iva)
        self.save()

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']


# class SaleProduct(models.Model):
#     sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
#     cant = models.IntegerField(default=0)
#     subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
#
#     def __str__(self):
#         return self.product.name
#
#     def toJSON(self):
#         item = model_to_dict(self, exclude=['sale'])
#         item['product'] = self.product.toJSON()
#         item['price'] = f'{self.price:.2f}'
#         item['subtotal'] = f'{self.subtotal:.2f}'
#         return item
#
#     class Meta:
#         verbose_name = 'Detalle de Venta'
#         verbose_name_plural = 'Detalle de Ventas'
#         default_permissions = ()
#         ordering = ['id']
