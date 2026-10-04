from django.urls import path
from . import views

urlpatterns = [
    # Nueva página principal que cargará al entrar a 127.0.0.1:8000/
    path('', views.inicio, name='inicio'), 
    
    # Movimos la cancha (el listado) a esta nueva ruta
    path('plantilla/', views.lista_jugadores, name='lista_jugadores'), 
    
    path('crear/', views.crear_jugador, name='crear_jugador'),
]