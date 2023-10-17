from audioop import avg
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from flask import request

from .dashboard import get_piechart, get_plot1

from .utils import get_plot, get_prediction
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
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
import cv2
from pyzbar.pyzbar import decode
from pydub import AudioSegment
from pydub.playback import play

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
    lista_productos = Producto.objects.all()
    print(settings.MEDIA_URL)
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
 
def editarProducto (request,producto_id):
    
    objProducto = Producto.objects.get(id=producto_id)

    if request.method == 'POST':
       frmProducto = ProductoForm(instance=objProducto)
       if frmProducto.is_valid():
            frmProducto.save()
            return redirect('/')   
    
    return render(request,'crearProducto.html',{'form':ProductoForm}) 
 
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




         