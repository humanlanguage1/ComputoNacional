from django.shortcuts import render, redirect
from django.conf import settings

from .models import Producto, Colaborador

#IMPORTANDO METODOS PARA AUTENTICACIÓN DE USUARIOS
from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.models import User
from inventarioComputo.forms import ColaboradorForm,UsuarioForm,ProductoForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    lista_productos = Producto.objects.all()
    print(settings.MEDIA_URL)
    context = {'lstProductos': lista_productos}
    return render(request,'index.html',context)

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
         