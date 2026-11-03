import json

from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import ensure_csrf_cookie

from .api_forms import JugadorAPIForm
from .models import Jugador


# Deje esta funcion para responder siempre con los mismos datos. Fran, tambien te sirve para el PUT. 
def jugador_a_json(jugador):
    return {
        'id': jugador.pk,
        'nombre': jugador.nombre,
        'apellido': jugador.apellido,
        'edad': jugador.edad,
        'posicion': jugador.posicion,
    }


# El GET deja la cookie CSRF lista para que despues podamos hacer el POST con X-CSRFToken. 
# Este CSRF no es el token del login; esa parte todavia hay que integrarla. 
@ensure_csrf_cookie
def jugadores_api(request):
    # Aqui traigo los jugadores de la misma base que usa la pagina, asi ambos muestran lo mismo. 
    if request.method == 'GET':
        jugadores = Jugador.objects.order_by('id')
        return JsonResponse([jugador_a_json(jugador) for jugador in jugadores], safe=False)

    # Por ahora deje GET y POST. Los otros metodos responden 405 y Allow indica cuales estan disponibles. 
    if request.method != 'POST':
        return JsonResponse(
            {'error': 'Metodo no permitido. Utiliza GET o POST.'},
            status=405,
            headers={'Allow': 'GET, POST'},
        )

    # Este POST recibe JSON; los formularios de la pagina siguen funcionando por su lado. 
    if request.content_type != 'application/json':
        return JsonResponse({'error': 'Utiliza Content-Type: application/json.'}, status=415)

    try:
        datos = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'error': 'El cuerpo debe contener JSON valido.'}, status=400)

    if not isinstance(datos, dict):
        return JsonResponse({'error': 'El JSON debe ser un objeto con los datos del jugador.'}, status=400)

    # Antes de guardar, reviso los campos obligatorios, los tipos, el largo de los textos y la edad. 
    form = JugadorAPIForm(datos)
    if not form.is_valid():
        return JsonResponse({'errors': form.errors.get_json_data()}, status=400)

    # Si todo esta bien, guardo en MySQL y devuelvo 201 con el jugador y su ruta en Location. 
    jugador = form.save()
    return JsonResponse(
        jugador_a_json(jugador),
        status=201,
        headers={'Location': reverse('api_jugador_detalle', args=[jugador.pk])},
    )


# Aqui busco por ID y devuelvo 404 si no existe. Fran, en esta vista puedes agregar PUT y DELETE. 
def jugador_api_detalle(request, jugador_id):
    if request.method != 'GET':
        return JsonResponse(
            {'error': 'Metodo no permitido. Utiliza GET.'},
            status=405,
            headers={'Allow': 'GET'},
        )

    try:
        jugador = Jugador.objects.get(pk=jugador_id)
    except Jugador.DoesNotExist:
        return JsonResponse({'error': 'Jugador no encontrado.'}, status=404)

    return JsonResponse(jugador_a_json(jugador))
