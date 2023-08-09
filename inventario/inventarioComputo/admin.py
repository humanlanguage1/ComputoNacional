from django.contrib import admin

from .models import Producto, Colaborador 
# Register your models here.


@admin.register(Producto)

class ProductoAdmin(admin.ModelAdmin):
    list_display= ('cod_empresa', 'cod_producto', 'cod_proveedor', 'cod_unidad_medida',
                   'cod_tipo_producto','cod_garantia','cod_linea_producto','cod_categoria',
                   'cod_marca','cod_presentacion','cod_procedencia','des_producto','des_adicional',
                   'des_tecnicas','des_info_adicional','num_parte','cod_barra','fec_registro',
                   'stk_minimo','stk_proveedor','pre_costo_promedio_anterior','pre_costo_promedio',
                   'pre_compra_base','pre_venta_base_anterior','pre_venta_base','pre_unitario_base_anterior',
                   'pre_unitario_base','pre_venta_oferta','pre_unitario_oferta','des_web_referencial',
                   'ind_servicio')
    
    list_display_links = ('cod_producto','des_producto','pre_venta_base')
    
    list_editable = ('cod_empresa', 'stk_minimo','pre_venta_oferta')
    
admin.site.register(Colaborador)

    
