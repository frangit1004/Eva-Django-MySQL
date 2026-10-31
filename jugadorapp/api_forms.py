from django import forms

from .forms import JugadorForm


# Aqui reutilice tu formulario y le agregue las validaciones que necesita la API. 
class JugadorAPIForm(JugadorForm):
    # Deje la edad entre 5 y 99 tambien en el servidor, para que no dependa del navegador. 
    edad = forms.IntegerField(
        min_value=5,
        max_value=99,
        error_messages={
            'required': 'La edad es obligatoria.',
            'invalid': 'La edad debe ser un numero entero.',
            'min_value': 'La edad debe ser mayor o igual a 5.',
            'max_value': 'La edad debe ser menor o igual a 99.',
        },
    )

    # Aqui reviso que lleguen textos y una edad entera, para no guardar tipos de datos que no corresponden. 
    def clean(self):
        cleaned_data = super().clean()
        for field in ('nombre', 'apellido', 'posicion'):
            value = self.data.get(field)
            if value is not None and not isinstance(value, str):
                self.add_error(field, 'Debe ser un texto.')

        edad = self.data.get('edad')
        if edad is not None and type(edad) is not int:
            self.add_error('edad', 'Debe ser un numero entero en JSON.')

        # Si mandan campos de mas, los rechazo; el ID lo tiene que generar la base de datos. 
        extra_fields = set(self.data) - set(self.fields)
        if extra_fields:
            self.add_error(None, 'Campos no permitidos: ' + ', '.join(sorted(extra_fields)))

        return cleaned_data
