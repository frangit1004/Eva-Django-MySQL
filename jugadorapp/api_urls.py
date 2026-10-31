from django.urls import path

from . import api_views


# Deje juntas las rutas de la API: GET/POST para jugadores y GET por ID, aparte de las rutas de la pagina. 
urlpatterns = [
    path('jugadores/', api_views.jugadores_api, name='api_jugadores'),
    path('jugadores/<int:jugador_id>/', api_views.jugador_api_detalle, name='api_jugador_detalle'),
]
