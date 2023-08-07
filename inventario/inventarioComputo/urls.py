from django.urls import path

from . import views

app_name = 'inventarioComputo'

urlpatterns = [
    path('', views.index,  name='index'),
    path('registro',views.registro, name='registro'),
    path('login', views.loginUsuario, name='login'), 
    path('producto/<int:producto_id>',views.producto,name='producto'),
]
