from django.shortcuts import get_object_or_404, render, redirect
from .models import Jugador
from .forms import JugadorForm

# --- PARTE DE FRANCISCO (C y R del CRUD) ---

# NUEVA: Página Principal (Home)
def inicio(request):
    return render(request, 'jugadorapp/inicio.html')

# Tarea R: Consultar (Leer)
def lista_jugadores(request):
    jugadores = Jugador.objects.all()
    return render(request, 'jugadorapp/lista_jugadores.html', {'jugadores': jugadores})

# Tarea C: Crear
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
def eliminar_jugador(request, jugador_id):
    jugador = get_object_or_404(Jugador, id=jugador_id)
    if request.method == 'POST':
        jugador.delete()
        return redirect('lista_jugadores')
    return render(request, 'jugadorapp/eliminar_jugador.html', {'jugador': jugador})
