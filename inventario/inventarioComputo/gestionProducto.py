class gestionProducto:
    def __init__(self,request):
        self.request = request
        self.session = request.session
        gestionar = self.session.get("gestionar")
        if not gestionar:
            gestionar = self.session["gestionar"] = {}
        self.gestionar = gestionar
        
    def add(self,producto,qty):
        if str(producto.cod_producto) not in self.cart.keys():
            self.cart[producto.cod_producto] = {
                "cod_empresa": producto.cod_empresa,
                "cod_producto": producto.cod_producto,
                "cod_proveedor": producto.cod_proveedor,
                "cod_unidad_medida": producto.cod_unidad_medida,
                "cod_tipo_producto": producto.cod_tipo_producto,
                "cod_garantia": producto.cod_garantia,
                "cod_linea_producto": producto.cod_linea_producto,
                "cod_categoria": producto.cod_categoria,
                "cod_marca": producto.cod_marca,
                "cod_presentacion": producto.cod_presentacion,
                "cod_procedencia": producto.cod_procedencia,
                "des_producto": producto.des_producto,
                "des_adicional": producto.des_adicional,
                "des_tecnicas": producto.des_tecnicas,
                "des_info_adicional": producto.des_info_adicional,
                "num_parte": producto.num_parte,
                "cod_barra": producto.cod_barra,
                "fec_registro": producto.fec_registro,
                "stk_minimo": producto.stk_minimo,
                "stk_proveedor": producto.stk_proveedor,
                "pre_costo_promedio_anterior": producto.pre_costo_promedio_anterior,
                "pre_costo_promedio": producto.pre_costo_promedio,
                "pre_compra_base": producto.pre_compra_base,
                "pre_venta_base_anterior": producto.pre_venta_base_anterior,
                "pre_venta_base": producto.pre_venta_base,
                "pre_unitario_base_anterior": producto.pre_unitario_base_anterior,
                "pre_unitario_base": producto.pre_unitario_base,
                "pre_venta_oferta": producto.pre_venta_oferta,
                "pre_unitario_oferta": producto.pre_unitario_oferta,
                "des_web_referencial": producto.des_web_referencial,
                "ind_servicio": producto.ind_Servicio,
                }
        self.save()
        
    def save(self):
        self.session["gestionar"] = self.gestionar
        self.session.modified = True
        
    def remove(self,producto):
        cod_producto = str(producto.cod_producto)
        if cod_producto in self.cart:
            del self.gestionar[cod_producto]
            self.save()
            
    def clear(self):
        self.session["gestionar"] = {}
        