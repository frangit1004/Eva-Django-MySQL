from django.contrib.auth import views as auth_views
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('api/token/', obtain_auth_token, name='api_token'),
    path('api/token/logout/', views.TokenLogoutAPIView.as_view(), name='api_logout'),
    path('api/jugadores/', views.JugadoresAPIView.as_view(), name='api_jugadores'),
    path('api/jugadores/<int:jugador_id>/', views.JugadorDetalleAPIView.as_view(), name='api_jugador_detalle'),
    path('login/', auth_views.LoginView.as_view(template_name='jugadorapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Nueva página principal que cargará al entrar a 127.0.0.1:8000/
    path('', views.inicio, name='inicio'), 
    
    # Movimos la cancha (el listado) a esta nueva ruta
    path('plantilla/', views.lista_jugadores, name='lista_jugadores'), 
    
    path('crear/', views.crear_jugador, name='crear_jugador'),

    # Rutas agregadas para conectar los botones Editar y Borrar con sus vistas. (MJ)
    path('editar/<int:jugador_id>/', views.editar_jugador, name='editar_jugador'),
    path('eliminar/<int:jugador_id>/', views.eliminar_jugador, name='eliminar_jugador'),
]
