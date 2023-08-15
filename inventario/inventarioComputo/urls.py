from django.urls import path

from . import views

app_name = 'inventarioComputo'

urlpatterns = [
    path('', views.index, name='index'),
    path('registro',views.registro,name='registro'),
    path('login',views.loginUsuario,name='login'),
    path('producto/<str:cod_producto>',views.producto,name='producto'),
    path('logout',views.logout_view,name='logout'),    
    path('gestionar',views.gestionar,name='gestionar')
]
