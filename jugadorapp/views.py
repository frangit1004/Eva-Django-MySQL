from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Jugador
from .forms import JugadorAPIForm, JugadorForm


# =========================================================
# AUTENTICACIÓN WEB + TOKEN EN MYSQL
# =========================================================

def login_web(request):
    if request.user.is_authenticated:
        return redirect('lista_jugadores')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            auth_login(request, usuario)
            # Genera o recupera el Token en MySQL al iniciar sesión en la web
            Token.objects.get_or_create(user=usuario)
            next_url = request.POST.get('next') or 'lista_jugadores'
            return redirect(next_url)
    else:
        form = AuthenticationForm()

    return render(request, 'jugadorapp/login.html', {'form': form})


@login_required
def logout_web(request):
    if request.method == 'POST':
        # Elimina el token del usuario en MySQL al cerrar sesión
        Token.objects.filter(user=request.user).delete()
        auth_logout(request)
    return redirect('login')


# =========================================================
# VISTAS INTERFAZ WEB (CRUD DE FRANCISCO Y MATÍAS)
# =========================================================

# --- PARTE DE FRANCISCO (C y R del CRUD) ---

def inicio(request):
    return render(request, 'jugadorapp/inicio.html')


@login_required
def lista_jugadores(request):
    jugadores = Jugador.objects.all().order_by('id')
    token_obj, _ = Token.objects.get_or_create(user=request.user)
    return render(request, 'jugadorapp/lista_jugadores.html', {
        'jugadores': jugadores,
        'user_token': token_obj.key
    })


@login_required
def crear_jugador(request):
    if request.method == 'POST':
        form = JugadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_jugadores')
    else:
        form = JugadorForm()
    return render(request, 'jugadorapp/crear_jugador.html', {'form': form})


# --- PARTE DE MATÍAS (U y D del CRUD) ---

@login_required
def editar_jugador(request, jugador_id):
    jugador = get_object_or_404(Jugador, id=jugador_id)
    if request.method == 'POST':
        form = JugadorForm(request.POST, instance=jugador)
        if form.is_valid():
            form.save()
            return redirect('lista_jugadores')
    else:
        form = JugadorForm(instance=jugador)
    return render(request, 'jugadorapp/editar_jugador.html', {'form': form, 'jugador': jugador})


@login_required
def eliminar_jugador(request, jugador_id):
    jugador = get_object_or_404(Jugador, id=jugador_id)
    if request.method == 'POST':
        jugador.delete()
        return redirect('lista_jugadores')
    return render(request, 'jugadorapp/eliminar_jugador.html', {'jugador': jugador})


# =========================================================
# ENDPOINTS API REST Y TOKEN (DRF)
# =========================================================

def jugador_a_json(jugador):
    return {
        'id': jugador.pk,
        'nombre': jugador.nombre,
        'apellido': jugador.apellido,
        'edad': jugador.edad,
        'posicion': jugador.posicion,
    }


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': 'Debes ingresar usuario y contraseña.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        usuario = authenticate(username=username, password=password)

        if usuario is not None:
            token, _ = Token.objects.get_or_create(user=usuario)
            return Response({
                'mensaje': 'Autenticación correcta',
                'usuario': usuario.username,
                'token': token.key
            }, status=status.HTTP_200_OK)

        return Response(
            {'error': 'Usuario o contraseña incorrectos.'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class TokenLogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()
        return Response(
            {'mensaje': 'Sesión cerrada y token eliminado correctamente.'},
            status=status.HTTP_200_OK
        )


class JugadoresAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # GET: Listar todos los jugadores
    def get(self, request):
        jugadores = Jugador.objects.order_by('id')
        return Response([jugador_a_json(j) for j in jugadores], status=status.HTTP_200_OK)

    # POST: Crear un nuevo jugador
    def post(self, request):
        datos = request.data
        if not isinstance(datos, dict):
            return Response(
                {'error': 'El cuerpo de la solicitud debe ser un objeto JSON válido.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        form = JugadorAPIForm(datos)
        if not form.is_valid():
            return Response(
                {'error': 'Datos inválidos', 'detalles': form.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        jugador = form.save()
        respuesta = jugador_a_json(jugador)
        respuesta['mensaje'] = 'Jugador creado correctamente'
        return Response(
            respuesta,
            status=status.HTTP_201_CREATED,
            headers={'Location': reverse('api_jugador_detalle', args=[jugador.pk])},
        )


class JugadorDetalleAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def obtener_jugador(self, jugador_id):
        try:
            return Jugador.objects.get(pk=jugador_id)
        except Jugador.DoesNotExist:
            return None

    # GET: Consultar un jugador por ID
    def get(self, request, jugador_id):
        jugador = self.obtener_jugador(jugador_id)
        if jugador is None:
            return Response(
                {'error': f'El jugador con ID {jugador_id} no existe.'},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(jugador_a_json(jugador), status=status.HTTP_200_OK)

    # PUT: Actualizar todos los datos de un jugador por ID
    def put(self, request, jugador_id):
        jugador = self.obtener_jugador(jugador_id)
        if jugador is None:
            return Response(
                {'error': f'El jugador con ID {jugador_id} no existe.'},
                status=status.HTTP_404_NOT_FOUND
            )

        datos = request.data
        if not isinstance(datos, dict):
            return Response(
                {'error': 'El cuerpo de la solicitud debe ser un objeto JSON válido.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        form = JugadorAPIForm(datos, instance=jugador)
        if not form.is_valid():
            return Response(
                {'error': 'Datos inválidos', 'detalles': form.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        jugador = form.save()
        respuesta = jugador_a_json(jugador)
        respuesta['mensaje'] = 'Jugador actualizado correctamente'
        return Response(respuesta, status=status.HTTP_200_OK)

    # PATCH: Actualizar parcialmente campos de un jugador por ID
    def patch(self, request, jugador_id):
        jugador = self.obtener_jugador(jugador_id)
        if jugador is None:
            return Response(
                {'error': f'El jugador con ID {jugador_id} no existe.'},
                status=status.HTTP_404_NOT_FOUND
            )

        datos_actualizados = {
            'nombre': request.data.get('nombre', jugador.nombre),
            'apellido': request.data.get('apellido', jugador.apellido),
            'edad': request.data.get('edad', jugador.edad),
            'posicion': request.data.get('posicion', jugador.posicion),
        }

        form = JugadorAPIForm(datos_actualizados, instance=jugador)
        if not form.is_valid():
            return Response(
                {'error': 'Datos inválidos', 'detalles': form.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        jugador = form.save()
        respuesta = jugador_a_json(jugador)
        respuesta['mensaje'] = 'Jugador actualizado parcialmente'
        return Response(respuesta, status=status.HTTP_200_OK)

    # DELETE: Eliminar un jugador por ID
    def delete(self, request, jugador_id):
        jugador = self.obtener_jugador(jugador_id)
        if jugador is None:
            return Response(
                {'error': f'El jugador con ID {jugador_id} no existe.'},
                status=status.HTTP_404_NOT_FOUND
            )

        jugador.delete()
        return Response(
            {'mensaje': f'Jugador con ID {jugador_id} eliminado correctamente.'},
            status=status.HTTP_200_OK
        )