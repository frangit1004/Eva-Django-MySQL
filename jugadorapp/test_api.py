import json

from django.test import Client, TestCase
from django.urls import reverse

from .models import Jugador


# Deje estas pruebas en una base aparte, asi podemos revisar la API sin tocar nuestros jugadores. 
class JugadorAPITests(TestCase):
    # Uso estos mismos datos en las pruebas para no tener que escribirlos cada vez. 
    def setUp(self):
        self.url = reverse('api_jugadores')
        self.datos = {
            'nombre': 'Matias',
            'apellido': 'Jeraldo',
            'edad': 18,
            'posicion': 'Delantero',
        }

    # Aqui reviso que el GET responda bien aunque todavia no tengamos jugadores. 
    def test_get_lista_vacia(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    # Compruebo que el GET traiga los datos del jugador sin cambiar lo que esta guardado. 
    def test_get_lista_jugadores(self):
        jugador = Jugador.objects.create(**self.datos)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{'id': jugador.pk, **self.datos}])
        self.assertEqual(Jugador.objects.count(), 1)

    # Esta prueba busca un solo jugador por su ID y revisa que vuelva en JSON. 
    def test_get_jugador_por_id(self):
        jugador = Jugador.objects.create(**self.datos)
        response = self.client.get(reverse('api_jugador_detalle', args=[jugador.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'id': jugador.pk, **self.datos})

    # Si el jugador no existe, tiene que responder 404 en JSON y no caerse la aplicacion. 
    def test_get_jugador_inexistente(self):
        response = self.client.get(reverse('api_jugador_detalle', args=[999999]))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'error': 'Jugador no encontrado.'})

    # Aqui reviso que el POST guarde de verdad y que el jugador aparezca en la API y en la pagina. 
    def test_post_crea_jugador_visible_en_api_y_web(self):
        response = self.client.post(self.url, self.datos, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        jugador = Jugador.objects.get(pk=response.json()['id'])
        self.assertEqual(response.json(), {'id': jugador.pk, **self.datos})
        for field, value in self.datos.items():
            self.assertEqual(getattr(jugador, field), value)
        self.assertEqual(self.client.get(response['Location']).json(), response.json())
        self.assertContains(self.client.get(reverse('lista_jugadores')), jugador.nombre)

    # Tambien probe las edades del limite: tanto 5 como 99 tienen que aceptarse. 
    def test_post_acepta_edades_limite(self):
        for edad in (5, 99):
            with self.subTest(edad=edad):
                response = self.client.post(
                    self.url, {**self.datos, 'edad': edad}, content_type='application/json',
                )
                self.assertEqual(response.status_code, 201)

    # Pruebo datos incorrectos para asegurarme de que no se guarden jugadores con errores. 
    def test_post_rechaza_datos_invalidos(self):
        invalidos = [
            {},
            *({**self.datos, 'edad': edad} for edad in (-1, 0, 4, 100, 999, '18', 'abc', 18.5, True, None, [])),
            *({**self.datos, field: value}
              for field in ('nombre', 'apellido', 'posicion')
              for value in ('', '   ', None, 123, True, [], {})),
            {**self.datos, 'nombre': 'x' * 101},
            {**self.datos, 'apellido': 'x' * 101},
            {**self.datos, 'posicion': 'x' * 51},
            {**self.datos, 'id': 123},
            {**self.datos, 'campo_desconocido': 'valor'},
        ]
        for datos in invalidos:
            with self.subTest(datos=datos):
                response = self.client.post(self.url, datos, content_type='application/json')
                self.assertEqual(response.status_code, 400)
                self.assertIn('errors', response.json())
                self.assertFalse(Jugador.objects.exists())

    # Si mandan el JSON vacio, incompleto o mal codificado, tiene que responder 400. 
    def test_post_rechaza_json_malformado(self):
        for body in ('', '{', '{"edad":}', b'\xff'):
            with self.subTest(body=body):
                # Dejo la cabecera incluso con el cuerpo vacio para probar ese caso tal como puede llegar. 
                response = self.client.post(
                    self.url, body, content_type='application/json', CONTENT_TYPE='application/json',
                )
                self.assertEqual(response.status_code, 400)
                self.assertIn('error', response.json())
        self.assertFalse(Jugador.objects.exists())

    # No basta con que sea JSON: tiene que venir un objeto con los campos del jugador. 
    def test_post_rechaza_json_que_no_es_objeto(self):
        for value in ([], 'texto', None, True, 18):
            with self.subTest(value=value):
                response = self.client.post(self.url, json.dumps(value), content_type='application/json')
                self.assertEqual(response.status_code, 400)
        self.assertFalse(Jugador.objects.exists())

    # Aqui reviso que el POST pida JSON y no acepte datos de formulario como si fueran lo mismo. 
    def test_post_rechaza_content_type_incorrecto(self):
        response = self.client.post(self.url, self.datos)
        self.assertEqual(response.status_code, 415)
        self.assertIn('error', response.json())
        self.assertFalse(Jugador.objects.exists())

    # Fran, cuando agregues PUT y DELETE hay que actualizar esta prueba; por ahora tienen que dar 405. 
    def test_metodos_no_implementados(self):
        jugador = Jugador.objects.create(**self.datos)
        detalle = reverse('api_jugador_detalle', args=[jugador.pk])
        for method in ('put', 'patch', 'delete'):
            for url, allowed in ((self.url, 'GET, POST'), (detalle, 'GET')):
                with self.subTest(method=method, url=url):
                    response = getattr(self.client, method)(url)
                    self.assertEqual(response.status_code, 405)
                    self.assertEqual(response['Allow'], allowed)
                    self.assertIn('error', response.json())
        response = self.client.post(detalle, self.datos, content_type='application/json')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(Jugador.objects.count(), 1)

    # Aqui pruebo CSRF de verdad: sin la cabecera el POST falla; con la cookie y la cabecera correctas guarda. 
    def test_post_conserva_proteccion_csrf(self):
        client = Client(enforce_csrf_checks=True)
        client.get(self.url)
        self.assertIn('csrftoken', client.cookies)
        response = client.post(self.url, self.datos, content_type='application/json')
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Jugador.objects.exists())
        response = client.post(
            self.url,
            self.datos,
            content_type='application/json',
            HTTP_X_CSRFTOKEN=client.cookies['csrftoken'].value,
        )
        self.assertEqual(response.status_code, 201)

    # Tambien reviso que las pantallas que ya teniamos sigan abriendo despues de agregar la API. 
    def test_pantallas_web_siguen_disponibles(self):
        jugador = Jugador.objects.create(**self.datos)
        urls = [
            reverse('inicio'),
            reverse('lista_jugadores'),
            reverse('crear_jugador'),
            reverse('editar_jugador', args=[jugador.pk]),
            reverse('eliminar_jugador', args=[jugador.pk]),
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)
