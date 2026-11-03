from django import forms
from .models import Jugador

# MATI: Esta clase crea un formulario HTML automáticamente basado en nuestro modelo Jugador.
# Tú puedes reutilizar este mismo formulario o crear uno nuevo para tu vista de "Editar", 
# pero recuerda que visualmente deben verse distintos según la pauta.
class JugadorForm(forms.ModelForm):
    class Meta:
        model = Jugador
        fields = '__all__' # Trae todos los campos (nombre, apellido, edad, posicion)
        
        # MATI: Los widgets le dan clases de Bootstrap a los inputs para que se vean bien en la página oscura
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del jugador'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido del jugador'}),
            # Validación numérica: La edad no puede ser menor a 5 años ni mayor a 99
            'edad': forms.NumberInput(attrs={'class': 'form-control', 'min': '5', 'max': '99'}),
            'posicion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Delantero, Defensa'}),
        }


class JugadorAPIForm(JugadorForm):
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

    def clean(self):
        cleaned_data = super().clean()
        for field in ('nombre', 'apellido', 'posicion'):
            value = self.data.get(field)
            if value is not None and not isinstance(value, str):
                self.add_error(field, 'Debe ser un texto.')

        edad = self.data.get('edad')
        if edad is not None and type(edad) is not int:
            self.add_error('edad', 'Debe ser un numero entero en JSON.')

        extra_fields = set(self.data) - set(self.fields)
        if extra_fields:
            self.add_error(None, 'Campos no permitidos: ' + ', '.join(sorted(extra_fields)))

        return cleaned_data