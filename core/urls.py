from django.urls import path
from .views import *
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', home, name="home" ),
    path('registro/', registro, name='registro'),
    path('registro_exitoso/', views.registro_exitoso, name='registro_exitoso'),
    path('iniciar_sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('login/', views.iniciar_sesion, name='login'), 
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('camiseta', camisetas, name="camiseta"),
    path('accesorio', accesorios, name="accesorio"),
    path('tour', tours, name="tour"),
    path('ticket', tickets, name="ticket"),
    path('addToCar/<codigo>', addToCar, name="addToCar"),
    path('delToCar/<codigo>', delToCar, name="delToCar"),
    path('zapatos', zapato, name="zapatos"),
    path('carrito/', carrito, name='carrito'),
    path('pagos/', pagos, name='pagos'),
    path('confirmacion_pago/', confirmacion_pago, name='confirmacion_pago'),
]
