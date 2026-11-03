from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Jugador
from .forms import JugadorAPIForm, JugadorForm

# --- PARTE DE FRANCISCO (C y R del CRUD) ---

# NUEVA: Página Principal (Home)
def inicio(request):
    return render(request, 'jugadorapp/inicio.html')

# Tarea R: Consultar (Leer)
@login_required
def lista_jugadores(request):
    jugadores = Jugador.objects.all()
    return render(request, 'jugadorapp/lista_jugadores.html', {'jugadores': jugadores})

# Tarea C: Crear
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

# --- PARTE DE MATIAS (U y D del CRUD) ---

# Tarea U: Actualizar datos de un jugador usando el mismo formulario del registro. (MJ)
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

# Tarea D: Confirmar y eliminar un jugador seleccionado de la plantilla. (MJ)
@login_required
def eliminar_jugador(request, jugador_id):
    jugador = get_object_or_404(Jugador, id=jugador_id)
    if request.method == 'POST':
        jugador.delete()
        return redirect('lista_jugadores')
    return render(request, 'jugadorapp/eliminar_jugador.html', {'jugador': jugador})


def jugador_a_json(jugador):
    return {
        'id': jugador.pk,
        'nombre': jugador.nombre,
        'apellido': jugador.apellido,
        'edad': jugador.edad,
        'posicion': jugador.posicion,
    }


class JugadoresAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        jugadores = Jugador.objects.order_by('id')
        return Response([jugador_a_json(jugador) for jugador in jugadores], status=status.HTTP_200_OK)

    def post(self, request):
        if not request.content_type or request.content_type.split(';', 1)[0].strip().lower() != 'application/json':
            return Response(
                {'error': 'Utiliza Content-Type: application/json.'},
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            )

        datos = request.data
        if not isinstance(datos, dict):
            return Response(
                {'error': 'El JSON debe ser un objeto con los datos del jugador.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        form = JugadorAPIForm(datos)
        if not form.is_valid():
            return Response({'errors': form.errors.get_json_data()}, status=status.HTTP_400_BAD_REQUEST)

        jugador = form.save()
        return Response(
            jugador_a_json(jugador),
            status=status.HTTP_201_CREATED,
            headers={'Location': reverse('api_jugador_detalle', args=[jugador.pk])},
        )


class JugadorDetalleAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, jugador_id):
        jugador = get_object_or_404(Jugador, pk=jugador_id)
        return Response(jugador_a_json(jugador), status=status.HTTP_200_OK)

    def put(self, request, jugador_id):
        jugador = get_object_or_404(Jugador, pk=jugador_id)
        if not request.content_type or request.content_type.split(';', 1)[0].strip().lower() != 'application/json':
            return Response(
                {'error': 'Utiliza Content-Type: application/json.'},
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            )

        datos = request.data
        if not isinstance(datos, dict):
            return Response(
                {'error': 'El JSON debe ser un objeto con los datos del jugador.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        form = JugadorAPIForm(datos, instance=jugador)
        if not form.is_valid():
            return Response({'errors': form.errors.get_json_data()}, status=status.HTTP_400_BAD_REQUEST)

        jugador = form.save()
        return Response(jugador_a_json(jugador), status=status.HTTP_200_OK)

    def delete(self, request, jugador_id):
        jugador = get_object_or_404(Jugador, pk=jugador_id)
        jugador.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TokenLogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
