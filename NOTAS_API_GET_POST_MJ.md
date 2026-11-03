# API de jugadores GET y POST 

Fran, aqui te deje mi parte del GET y POST para la tercera evaluacion. La idea es seguir con el proyecto que ya teniamos, usando el mismo modelo Jugador y la conexion MySQL de settings.py. Mantuvimos tus pantallas y el estilo, y para esto no hizo falta instalar nada mas ni cambiar las migraciones. (MJ)

## Que deje en cada archivo 

- jugadorapp/api_views.py: aqui esta la logica. El GET trae todos los jugadores o uno por ID, y el POST revisa los datos y guarda al jugador. Deje jugador_a_json para que las respuestas tengan siempre los mismos campos. (MJ)
- jugadorapp/api_forms.py: reutilice tu JugadorForm y le agregue las validaciones para JSON. La edad tiene que ser un entero entre 5 y 99, y si llegan campos que no corresponden se rechazan. Tu formulario web quedo como estaba. (MJ)
- jugadorapp/api_urls.py: deje las rutas de la API juntas para que despues podamos agregar tu parte sin enredarnos con las rutas de la pagina. (MJ)
- jugadorapp/urls.py: aqui conecte las rutas nuevas bajo /api/. (MJ)
- jugadorapp/test_api.py: deje las pruebas del GET, POST, errores y CSRF. Tambien revisan que las pantallas anteriores sigan abriendo. Todo esto se prueba en una base aparte. (MJ)

## Rutas para que podamos seguir con tu parte 

| Metodo | Ruta | Resultado |
| --- | --- | --- |
| GET | /api/jugadores/ | Trae la lista en JSON con 200. Si esta vacia, devuelve []. (MJ) |
| GET | /api/jugadores/1/ | Trae ese jugador con 200; si no existe, responde 404 en JSON. (MJ) |
| POST | /api/jugadores/ | Guarda al jugador y devuelve 201. En Location queda su ruta por ID. (MJ) |

Para el POST hay que mandar Content-Type: application/json con nombre, apellido, edad y posicion. Los textos son obligatorios y tienen el largo maximo que ya define el modelo. Ojo con la edad: va como numero entero, sin comillas, y tampoco acepta booleanos. Si los datos o el JSON vienen mal, responde 400; si el tipo de contenido no corresponde, 415. Los metodos que todavia no agregamos responden 405 y Allow indica cuales se pueden usar. (MJ)

```json
{
  "nombre": "Matias",
  "apellido": "Jeraldo",
  "edad": 18,
  "posicion": "Delantero"
}
```

Asi puedes mandar el JSON del POST. El ID no lo agregues, porque lo genera la base de datos al guardar. 

## Como probarlo en PowerShell (MJ)

Primero hay que tener MySQL iniciado, la base creada y las migraciones aplicadas. Desde la carpeta donde esta manage.py puedes levantar Django con este comando. Te deje los ejemplos para ejecutarlos cuando quieras probar; no se ejecutan solos. (MJ)

```powershell
# Con esto levantamos Django para probar la API. 
python -B manage.py runserver
```

Despues abre otra terminal. Primero hacemos el GET y guardamos la cookie CSRF en la sesion de PowerShell. Para el POST usamos esa misma cookie y la cabecera X-CSRFToken. Ojo aqui para no confundirnos: este CSRF no es el token del login que pide la pauta. (MJ)

```powershell
# Primero traemos los jugadores y dejamos lista la cookie CSRF. 
$apiUrl = 'http://127.0.0.1:8000/api/jugadores/'
Invoke-RestMethod -Uri $apiUrl -SessionVariable apiSesion
$apiCsrf = $apiSesion.Cookies.GetCookies([uri]$apiUrl)['csrftoken'].Value

# Este POST si guarda un jugador real en MySQL con los datos de abajo. 
$apiDatos = @{
    nombre = 'Matias'
    apellido = 'Jeraldo'
    edad = 18
    posicion = 'Delantero'
} | ConvertTo-Json
$apiJugador = Invoke-RestMethod -Uri $apiUrl -Method Post -WebSession $apiSesion `
    -ContentType 'application/json' -Headers @{ 'X-CSRFToken' = $apiCsrf } -Body $apiDatos
$apiJugador

# Ahora buscamos por ID al jugador que acabamos de crear. 
Invoke-RestMethod -Uri ($apiUrl + $apiJugador.id + '/') -WebSession $apiSesion
```

El jugador que crees tambien tiene que aparecer en /plantilla/. Con este SELECT puedes revisar MySQL y mostrar que la pagina y la API estan usando los mismos datos. Recuerda que el POST del ejemplo guarda de verdad, asi que usa datos que quieras dejar en la base. (MJ)

```sql
-- Con esto revisamos los jugadores guardados en la tabla. 
SELECT id, nombre, apellido, edad, posicion FROM jugadorapp_jugador ORDER BY id;
```

## Pruebas que deje listas 

Para estas pruebas, Django crea una base aparte llamada test_escuela_deportiva_bd y la elimina cuando termina. Asi no tocamos los jugadores de escuela_deportiva_bd. Eso si, el usuario de MySQL necesita permisos para crear esa base de pruebas. (MJ)

```powershell
# Con este comando puedes volver a correr las pruebas del GET y POST. 
python -B manage.py test jugadorapp.test_api --noinput
```

Quedaron pasando las 13 pruebas en MariaDB, incluyendo guardar un jugador en la base de pruebas y verlo desde la API y la pagina. Al terminar se elimino esa base temporal y quedo intacto el jugador que ya teniamos en la base del proyecto. manage.py check salio sin errores. Al revisar MySQL sigue apareciendo el aviso que ya estaba sobre el modo estricto desactivado; esa configuracion la deje como estaba. (MJ)

## Lo que falta integrar entre los dos 

Mi parte de esta entrega quedo en GET y POST. Todavia faltan PUT y DELETE de la API, login, logout, generar el token y restringir el acceso. Por ahora estos endpoints no piden iniciar sesion, asi que aun tenemos que integrar eso para completar lo de la pauta. (MJ)

Fran, puedes seguir en jugador_api_detalle para agregar PUT y DELETE, y reutilizar jugador_a_json y JugadorAPIForm. Cuando lo hagas, acuerdate de actualizar Allow y las pruebas que ahora esperan 405 para esos metodos. Para el login/token hay que proteger las vistas de la API y probar que pasa con un token correcto, uno incorrecto y sin token. Dejemos CSRF activo hasta integrar bien la autenticacion. (MJ)

Todo esto quedo en la rama codex/eva03-get-post. Te deje los comentarios con (MJ) para que ubiques facil lo que agregue y como funciona. (MJ)
