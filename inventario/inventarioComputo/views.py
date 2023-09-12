from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse

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
# Create your views here.
def index(request):
    lista_productos = Producto.objects.all()
    print(settings.MEDIA_URL)
    context = {'lstProductos': lista_productos}
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






         