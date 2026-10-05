from django.urls import path
from . import views

urlpatterns = [
    # Nueva página principal que cargará al entrar a 127.0.0.1:8000/
    path('', views.inicio, name='inicio'), 
    
    # Movimos la cancha (el listado) a esta nueva ruta
    path('plantilla/', views.lista_jugadores, name='lista_jugadores'), 
    
    path('crear/', views.crear_jugador, name='crear_jugador'),

    # Rutas agregadas para conectar los botones Editar y Borrar con sus vistas. (MJ)
    path('editar/<int:jugador_id>/', views.editar_jugador, name='editar_jugador'),
    path('eliminar/<int:jugador_id>/', views.eliminar_jugador, name='eliminar_jugador'),
]
