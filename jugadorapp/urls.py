from django.urls import include, path
from . import views

urlpatterns = [
    # Aqui conecte la API de GET y POST bajo /api/, para tener sus rutas ordenadas aparte de la pagina. (MJ)
    path('api/', include('jugadorapp.api_urls')),

    # Nueva página principal que cargará al entrar a 127.0.0.1:8000/
    path('', views.inicio, name='inicio'), 
    
    # Movimos la cancha (el listado) a esta nueva ruta
    path('plantilla/', views.lista_jugadores, name='lista_jugadores'), 
    
    path('crear/', views.crear_jugador, name='crear_jugador'),

    # Rutas agregadas para conectar los botones Editar y Borrar con sus vistas. (MJ)
    path('editar/<int:jugador_id>/', views.editar_jugador, name='editar_jugador'),
    path('eliminar/<int:jugador_id>/', views.eliminar_jugador, name='eliminar_jugador'),
]
