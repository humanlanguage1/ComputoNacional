from django.urls import path

from . import views 


app_name = 'inventarioComputo'

urlpatterns = [
    path('', views.index, name='index'),
    #re_path(r"^serviceworker\.js$", service_worker, name="serviceworker"),
    path('registro',views.registro,name='registro'),
    path('producto/<int:producto_id>',views.producto,name='producto'),
    path('listaProd',views.listaProd,name='listaProd'),
    path('crearProducto',views.crearProducto,name='crearProducto'),   
    path('editarProducto/<int:producto_id>',views.editarProducto,name='editarProducto'),
    path('eliminarProducto/<int:producto_id>',views.eliminarProducto,name='eliminarProducto'),
    path('reporte', views.reporte, name='reporte'),
    path('prediccion', views.prediccion, name='prediccion'),
    path('dashboard', views.dashboard, name='dashboard'),
]
