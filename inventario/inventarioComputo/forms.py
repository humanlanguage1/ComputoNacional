from django import forms
from django.forms import ModelForm
from .models import Producto

class UsuarioForm(forms.Form):
    usuario = forms.CharField(max_length=20,required=True)
    clave = forms.CharField(widget=forms.PasswordInput)

class ColaboradorForm(forms.Form):
    doc_ide = forms.CharField(label='DNI',max_length=20,required=True)
    nombres = forms.CharField(max_length=200,required=True)
    apellidos = forms.CharField(max_length=200,required=True)
    correo = forms.EmailField(required=True)
    telefono = forms.CharField(max_length=20,required=False)
    usuario = forms.CharField(max_length=20,required=True)
    clave = forms.CharField(widget=forms.PasswordInput)    
    
class ProductoForm(ModelForm):
    cod_empresa = forms.CharField(max_length=2,required=True)
    cod_producto= forms.CharField(max_length=100, required=True) 
    cod_proveedor = forms.CharField(max_length=11, required=False)
    cod_unidad_medida = forms.CharField(max_length=3, required=False)
    cod_tipo_producto = forms.IntegerField()
    cod_garantia = forms.CharField(max_length=3)
    cod_linea_producto = forms.CharField(max_length=5)
    cod_categoria = forms.CharField(max_length=3)
    cod_marca = forms.CharField(max_length=5)
    cod_presentacion = forms.CharField(max_length=3)
    cod_procedencia = forms.CharField(max_length=3)
    des_producto = forms.CharField(max_length=255)
    des_adicional = forms.CharField(widget=forms.Textarea)
    des_tecnicas = forms.CharField(widget=forms.Textarea)
    des_info_adicional = forms.CharField(widget=forms.Textarea)
    num_parte = forms.CharField(max_length=50)
    cod_barra = forms.CharField(max_length=15)
    fec_registro = forms.DateField()
    stk_minimo = forms.FloatField()
    stk_proveedor = forms.FloatField()
    pre_costo_promedio_anterior = forms.FloatField()
    pre_costo_promedio = forms.FloatField()
    pre_compra_base = forms.FloatField()
    pre_venta_base_anterior = forms.FloatField()
    pre_venta_base = forms.FloatField()
    pre_unitario_base_anterior = forms.FloatField()
    pre_unitario_base = forms.FloatField()
    pre_venta_oferta = forms.FloatField()
    pre_unitario_oferta = forms.FloatField()
    des_web_referencial = forms.CharField(max_length=255)
    ind_servicio = forms.CharField(max_length=1)
    ind_autogenerado = forms.CharField(max_length=1)
    ind_lote_serie1 = forms.CharField(max_length=1)
    ind_activo_web = forms.CharField(max_length=1)
    ind_mostrar_portal = forms.CharField(max_length=1)
    ind_catalogo = forms.CharField(max_length=1)
    ind_lote = forms.CharField(max_length=1)
    ind_importado = forms.CharField(max_length=1)
    ind_activo = forms.CharField(max_length=1)
    code_user_insert = forms.CharField(max_length=10)
    date_insert = forms.DateField()
    code_user_last_update = forms.CharField(max_length=10)
    date_last_update = forms.DateField()
    ind_serie = forms.CharField(max_length=1)
    class Meta:
       model = Producto
       fields = '__all__' 


    

      
    