from django.shortcuts import render, redirect
from django.conf import settings

from .models import Producto, Colaborador
from inventarioComputo import gestionProducto

#IMPORTANDO METODOS PARA AUTENTICACIÓN DE USUARIOS
from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.models import User
from inventarioComputo.forms import ColaboradorForm,UsuarioForm
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
     
def loginUsuario(request):
    frmUsuario = UsuarioForm()
    
    if request.method == 'POST':
        frmLogin = UsuarioForm(request.POST)
        
        if frmLogin.is_valid():
            data = frmLogin.cleaned_data
            dataUsuario = data['usuario']
            dataPassword = data['clave']
            
            loginUsuario = authenticate(request,username=dataUsuario,password=dataPassword)
            if loginUsuario is not None:
                print("ok")
                login(request,loginUsuario)
                return render(request,'cuenta.html')
            else:
                print("error")
                context = {
                    'form':frmUsuario,
                    'error':'datos erroneos'
                }
                return render(request,'login.html',context)
            
    
    context = {
        'form':frmUsuario
    }
    return render(request,'login.html',context)     

def producto(request,cod_producto):
    objProducto = Producto.objects.get(id=cod_producto) 
    #equivalente a : select * from producto where id = producto_id
    context = {
        "producto":objProducto
    }
    return render(request,'producto.html',context)

def agregarProd(request,cod_producto):
    objProducto = Producto.objects.get(id=cod_producto)
    gestionarProd = gestionProducto(request)
    gestionarProd.add(objProducto,1)
    print(request.session.get("gestionar"))
    return render(request,'gestionProducto.html')

def eliminarProducto(request):
    objProducto = Producto.objects.get(id=cod_producto)
    gestionarProd = gestionProducto(request)
    gestionarProd.add(objProducto) 
    print(request.session.get("gestionar"))
    return render(request, 'gestionProducto.html')

            
def gestionar(request):
    print(request.session.get("gestionProducto"))
    return render(request,'gestionProducto.html')
    
@login_required
def logout_view(request):
    """Logout a user."""
    logout(request)
    return redirect('/login')    