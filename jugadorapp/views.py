from django.shortcuts import render, redirect
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