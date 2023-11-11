from audioop import avg
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from flask import request

from .dashboard import get_piechart, get_plot1

from .utils import get_plot, get_prediction, render_to_pdf
from .models import Producto, Colaborador
from django.conf import settings
from django.views.generic.base import TemplateView
#IMPORTANDO METODOS PARA AUTENTICACIÓN DE USUARIOS
from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.models import User
from inventarioComputo.forms import ColaboradorForm,UsuarioForm,ProductoForm
from django.contrib.auth.decorators import login_required
import pandas as pd 
from django.db.models import Avg
from django.db.models import Q
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
import cv2
from pyzbar.pyzbar import decode
from pydub import AudioSegment
from pydub.playback import play
# Import PDF Stuff
from django.http import FileResponse
from django.views.generic import View
import io
import reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter


# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):
    labels = []
    data = []
    labels1 = []
    data1 = []
    lista_productos = Producto.objects.all()
    lista_usuarios = User.objects.all()
    print(settings.MEDIA_URL)
    qs= Producto.objects.all()
    queryset= Producto.objects.order_by('-stk_minimo')[:5]
    queryset1= Producto.objects.order_by('-pre_venta_oferta')[:5]
    for producto in queryset:
        labels.append(producto.cod_producto)
        data.append(producto.stk_minimo)
        
    for producto in queryset1:
        labels1.append(producto.cod_producto)
        data1.append(producto.pre_venta_oferta)       
   # promedio_stock = qs.aggregate(Avg('stk_minimo'))
    total_stock = 0
    for item in qs:
        total_stock += item.stk_minimo
    x = [x.cod_producto for x in qs]
    y = [y.cod_categoria for y in qs]   
    tabla = get_plot1(x,y)  
    context = {'lstProductos': lista_productos,
               'tabla': tabla,
              # 'piechart': piechart,
               'total_stock': total_stock,
               'lista_usuarios': lista_usuarios,
               'labels': labels,
               'data': data,
               'labels1': labels1,
               'data1': data1,
               }
    
    return render(request,'index.html',context)


def listaProd(request):
    busqueda = request.POST.get("buscar")
    lista_productos = Producto.objects.all()
    print(settings.MEDIA_URL)
    
    if busqueda: 
        lista_productos = Producto.objects.filter(
           Q(id__icontains=busqueda) |
           Q(cod_producto__icontains= busqueda) |
           Q(des_producto__icontains= busqueda)
        ).distinct() 
        
    context = {'lstProductos': lista_productos}
    return render(request,'listaProd.html',context)

def registro(request):
    frmColaborador = ColaboradorForm()
    
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        frmNuevoColaborador = ColaboradorForm(request.POST)
        # check whether it's valid:
        if frmColaborador.is_valid():
            data = frmNuevoColaborador.cleaned_data
            dataUsuario = data['usuario']
            dataPassword = data['clave']
            #creamos usuarios
            nuevoUsuario = User.objects.create_user(username=dataUsuario,password=dataPassword)
 
            nuevoUsuario.first_name = data['nombres']
            nuevoUsuario.last_name = data['apellidos']
            nuevoUsuario.email = data['correo']
            nuevoUsuario.save()       
            
            nuevoColaborador = Colaborador (usuario=nuevoUsuario)
            nuevoColaborador.telefono = data['telefono']
            nuevoColaborador.doc_ide = data['doc_ide']
            nuevoColaborador.save()
            
            return render(request,'graciasRegistro.html')
     
    context = {
         'frmColaborador': frmColaborador
     }     
    return render(request,'registroColaborador.html',context)  

def producto(request,producto_id):  
    objProducto = Producto.objects.get(id=producto_id) 
    #equivalente a : select * from producto where id = producto_id
    context = {
        "producto":objProducto
    }
    return render(request,'producto.html',context)

def crearProducto (request):
    if request.POST:
     frmProducto = ProductoForm(request.POST)
     
     if frmProducto.is_valid():
        frmProducto.save()
        return redirect('/')
     
    return render(request,'crearProducto.html',{'form':ProductoForm})

def edicionProducto(request,producto_id):
    producto = Producto.objects.get(id=producto_id) 
    form = ProductoForm(request.POST or None, instance = producto)
    if form.is_valid():
        form.save()
        return redirect('/listaProd')
    return render(request, "edicionProducto.html", {'producto': producto, 'form':form})    
 
def editarProducto (request):
    
    cod_empresa  = request.POST['cod_empresa']
    cod_producto  = request.POST['cod_producto']
    cod_proveedor  = request.POST['cod_proveedor']
    cod_unidad_medida  = request.POST['cod_unidad_medida']
    cod_tipo_producto  = request.POST['cod_tipo_producto']
    cod_garantia = request.POST['cod_garantia']
    cod_linea_producto = request.POST['cod_linea_producto']
    cod_categoria = request.POST['cod_categoria']
    cod_marca = request.POST['cod_marca']
    cod_presentacion = request.POST['cod_presentacion']
    cod_procedencia = request.POST['cod_procedencia']
    des_producto = request.POST['des_producto']
    des_adicional = request.POST['des_adicional']
    des_tecnicas = request.POST['des_tecnicas']
    des_info_adicional = request.POST['des_info_adicional']
    num_parte = request.POST['num_parte']
    cod_barra = request.POST['cod_barra']
    fec_registro = request.POST['fec_registro']
    stk_minimo = request.POST['stk_minimo']
    stk_proveedor = request.POST['stk_proveedor']
    pre_costo_promedio_anterior = request.POST['pre_costo_promedio_anterior']
    pre_costo_promedio = request.POST['pre_costo_promedio']
    pre_compra_base = request.POST['pre_compra_base']
    pre_venta_base_anterior = request.POST['pre_venta_base_anterior']
    pre_venta_base = request.POST['pre_venta_base']
    pre_unitario_base_anterior = request.POST['pre_unitario_base_anterior']
    pre_unitario_base = request.POST['pre_unitario_base']
    pre_venta_oferta = request.POST['pre_venta_oferta']
    pre_unitario_oferta = request.POST['pre_unitario_oferta']
    des_web_referencial = request.POST['des_web_referencial']
    ind_servicio = request.POST['ind_servicio']
    ind_autogenerado = request.POST['ind_autogenerado']
    ind_lote_serie1 = request.POST['ind_lote_serie1']
    ind_activo_web = request.POST['ind_activo_web']
    ind_mostrar_portal = request.POST['ind_mostrar_portal']
    ind_catalogo = request.POST['ind_catalogo']
    ind_lote = request.POST['ind_lote']
    ind_importado = request.POST['ind_importado']
    ind_activo = request.POST['ind_activo']
    code_user_insert = request.POST['code_user_insert']
    date_insert = request.POST['date_insert']
    code_user_last_update = request.POST['code_user_last_update']
    date_last_update = request.POST['date_last_update']
    ind_serie = request.POST['ind_serie']
    
    p = Producto.objects.get(cod_producto=cod_producto)
    p.cod_empresa = cod_empresa
    p.cod_producto = cod_producto
    p.cod_proveedor = cod_proveedor
    p.cod_unidad_medida = cod_unidad_medida 
    p.cod_tipo_producto = cod_tipo_producto  
    p.cod_garantia = cod_garantia 
    p.cod_linea_producto = cod_linea_producto 
    p.cod_categoria = cod_categoria 
    p.cod_marca = cod_marca  
    p.cod_presentacion = cod_presentacion  
    p.cod_procedencia = cod_procedencia 
    p.des_producto = des_producto 
    p.des_adicional = des_adicional 
    p.des_tecnicas = des_tecnicas 
    p.des_info_adicional = des_info_adicional 
    p.num_parte = num_parte 
    p.cod_barra = cod_barra  
    p.fec_registro = fec_registro 
    p.stk_minimo = stk_minimo 
    p.stk_proveedor = stk_proveedor 
    p.pre_costo_promedio_anterior = pre_costo_promedio_anterior 
    p.pre_costo_promedio = pre_costo_promedio 
    p.pre_compra_base = pre_compra_base 
    p.pre_venta_base_anterior = pre_venta_base_anterior 
    p.pre_venta_base = pre_venta_base 
    p.pre_unitario_base_anterior = pre_unitario_base_anterior 
    p.pre_unitario_base = pre_unitario_base 
    p.pre_venta_oferta = pre_venta_oferta 
    p.pre_unitario_oferta = pre_unitario_oferta  
    p.des_web_referencial = des_web_referencial 
    p.ind_servicio = ind_servicio 
    p.ind_autogenerado = ind_autogenerado 
    p.ind_lote_serie1 = ind_lote_serie1 
    p.ind_activo_web = ind_activo_web  
    p.ind_activo_web = ind_mostrar_portal  
    p.ind_catalogo = ind_catalogo 
    p.ind_lote = ind_lote 
    p.ind_importado = ind_importado 
    p.ind_activo = ind_activo 
    p.code_user_insert = code_user_insert 
    p.date_insert = date_insert 
    p.code_user_last_update = code_user_last_update 
    p.date_last_update = date_last_update 
    p.ind_serie = ind_serie 
    p.save()
    
    return redirect('/')
 
def eliminarProducto(request,producto_id):
    objProducto = Producto.objects.get(id=producto_id)
       
    
    if request.method == 'POST':
         objProducto.delete()  
         return redirect('/')

    context= {'item':objProducto}
    return render(request,'eliminarProducto.html',context) 

#metodos para visualizar los gráficos
def reporte(request):
    qs= Producto.objects.all()
    x = [x.cod_producto for x in qs]
    y = [y.stk_minimo for y in qs]   
    chart = get_plot(x,y) 
    return render(request, 'reporte.html', {'chart':chart})


def prediccion(request):
    qs= Producto.objects.all()
    x = [x.stk_minimo for x in qs]
    y = [y.stk_proveedor for y in qs]   
    chart = get_prediction(x,y) 
    return render(request, 'prediccion.html', {'chart':chart})   

def dashboard(request):

    pass

def verCodigoBarras(request):
    video= cv2.VideoCapture(1)
    success, frame = video.read()
    detector = cv2.barcode.BarcodeDetector()
    
    while video.isOpened():
        while success:
            cv2.imshow('frame', frame)
            detectedBarcode = decode(frame)
            if cv2.waitKey(1) == ord('q'):
                break
            success, frame = video.read()
            if not detectedBarcode:
                print("No any Barcode Detected")
            else:
        # codes in barcode 
                for barcode in detectedBarcode:
                    # if barcode is not blank 
                    if barcode.data != "":
                        detectedBarcode = decode(frame)
                        cv2.putText(frame,str(barcode.data),(50,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,255),2)
                        cv2.imwrite("barcode.png",frame)
                        
                                    
        text = str(barcode.data)
        video.release()
        cv2.destroyAllWindows()
        context = {
            "text" : text
        }
    
    return render(request, 'verCodigoBarras.html', context)

def nosotros (request):
    return render(request, 'nosotros.html')

def verPdf(request):
	# Create Bytestream buffer
        buf = io.BytesIO()
        # Create a canvas
        c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
        # Create a text object
        textob = c.beginText()
        textob.setTextOrigin(0.5*inch, 0.5*inch)
        textob.setFont("Helvetica", 8)

        # Add some lines of text
        #lines = [
        #	"This is line 1",
        #	"This is line 2",
        #	"This is line 3",
        #]
        
        # Designate The Model
        productos = Producto.objects.all()

        # Create blank list
        lines = []

        for producto in productos:
            lines.append(producto.des_producto)
            lines.append(str(producto.fec_registro))
            lines.append(str(producto.pre_venta_oferta))
            lines.append(" ")

        # Loop
        for line in lines:
            textob.textLine(line)

        # Finish Up
        c.drawText(textob)
        c.showPage()
        c.save()
        buf.seek(0)
            
        return FileResponse(buf, as_attachment=True, filename='productos.pdf')


   
                
            
        

    




         