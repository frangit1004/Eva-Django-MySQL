from django.urls import path
from . import views

urlpatterns = [
    # ENDPOINTS API REST AUTENTICACIÓN TOKEN (compatibles con ambas rutas)
    path('api/login/', views.LoginAPIView.as_view(), name='api_login'),
    path('api/token/', views.LoginAPIView.as_view(), name='api_token'),
    path('api/logout/', views.TokenLogoutAPIView.as_view(), name='api_logout'),
    path('api/token/logout/', views.TokenLogoutAPIView.as_view(), name='api_token_logout'),

    # ENDPOINTS API REST JUGADORES (GET, POST, PUT, PATCH, DELETE)
    path('api/jugadores/', views.JugadoresAPIView.as_view(), name='api_jugadores'),
    path('api/jugadores/<int:jugador_id>/', views.JugadorDetalleAPIView.as_view(), name='api_jugador_detalle'),

    # RUTAS AUTENTICACIÓN WEB (Generan y eliminan el Token sincronizado)
    path('login/', views.login_web, name='login'),
    path('logout/', views.logout_web, name='logout'),

    # RUTAS INTERFAZ WEB (CRUD)
    path('', views.inicio, name='inicio'),
    path('plantilla/', views.lista_jugadores, name='lista_jugadores'),
    path('crear/', views.crear_jugador, name='crear_jugador'),
    path('editar/<int:jugador_id>/', views.editar_jugador, name='editar_jugador'),
    path('eliminar/<int:jugador_id>/', views.eliminar_jugador, name='eliminar_jugador'),
]