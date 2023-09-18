# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import DecimalField, IntegerField, CharField
from django.db.models import Avg


class Producto(models.Model):
    cod_empresa = models.CharField(max_length=2)
    cod_producto = models.CharField(max_length=100)
    cod_proveedor = models.CharField(max_length=11, blank=True, null=True)
    cod_unidad_medida = models.CharField(max_length=3, blank=True, null=True)
    cod_tipo_producto = models.IntegerField()
    cod_garantia = models.CharField(max_length=3, blank=True, null=True)
    cod_linea_producto = models.CharField(max_length=5)
    cod_categoria = models.CharField(max_length=3, blank=True, null=True)
    cod_marca = models.CharField(max_length=5, blank=True, null=True)
    cod_presentacion = models.CharField(max_length=3, blank=True, null=True)
    cod_procedencia = models.CharField(max_length=3, blank=True, null=True)
    des_producto = models.CharField(max_length=255)
    des_adicional = models.TextField(blank=True, null=True)
    des_tecnicas = models.TextField(blank=True, null=True)
    des_info_adicional = models.TextField(blank=True, null=True)
    num_parte = models.CharField(max_length=50, blank=True, null=True)
    cod_barra = models.CharField(max_length=15, blank=True, null=True)
    fec_registro = models.DateField()
    stk_minimo = models.FloatField()
    stk_proveedor = models.FloatField()
    pre_costo_promedio_anterior = models.FloatField()
    pre_costo_promedio = models.FloatField()
    pre_compra_base = models.FloatField()
    pre_venta_base_anterior = models.FloatField()
    pre_venta_base = models.FloatField()
    pre_unitario_base_anterior = models.FloatField()
    pre_unitario_base = models.FloatField()
    pre_venta_oferta = models.FloatField()
    pre_unitario_oferta = models.FloatField()
    des_web_referencial = models.CharField(max_length=255)
    ind_servicio = models.CharField(max_length=1)
    ind_autogenerado = models.CharField(max_length=1)
    ind_lote_serie1 = models.CharField(max_length=1)
    ind_activo_web = models.CharField(max_length=1)
    ind_mostrar_portal = models.CharField(max_length=1)
    ind_catalogo = models.CharField(max_length=1)
    ind_lote = models.CharField(max_length=1)
    ind_importado = models.CharField(max_length=1)
    ind_activo = models.CharField(max_length=1)
    code_user_insert = models.CharField(max_length=10)
    date_insert = models.DateField(blank=True, null=True)
    code_user_last_update = models.CharField(max_length=10, blank=True, null=True)
    date_last_update = models.DateField(blank=True, null=True)
    ind_serie = models.CharField(max_length=1)

    def _str__(self):
        return self.name
    

class Colaborador(models.Model):
    usuario = models.OneToOneField(User,on_delete=models.RESTRICT)
    doc_ide = models.CharField(max_length=20,unique=True)
    correo = models.CharField(max_length=200,blank=True)
    telefono = models.CharField(max_length=20,blank=True)
    
    def __str__(self):
        return self.usuario.first_name