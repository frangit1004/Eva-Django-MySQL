from django import forms
from .models import Jugador

# MATI: Esta clase crea un formulario HTML automáticamente basado en nuestro modelo Jugador.
# Tú puedes reutilizar este mismo formulario o crear uno nuevo para tu vista de "Editar", 
# pero recuerda que visualmente deben verse distintos según la pauta.
class JugadorForm(forms.ModelForm):
    edad = forms.IntegerField(
        min_value=5,
        max_value=99,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '5', 'max': '99'}),
        error_messages={
            'required': 'La edad es obligatoria.',
            'invalid': 'La edad debe ser un número entero.',
            'min_value': 'La edad debe ser mayor o igual a 5 años.',
            'max_value': 'La edad debe ser menor o igual a 99 años.',
        },
    )

    class Meta:
        model = Jugador
        fields = '__all__' # Trae todos los campos (nombre, apellido, edad, posicion)
        
        # MATI: Los widgets le dan clases de Bootstrap a los inputs para que se vean bien en la página oscura
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del jugador'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido del jugador'}),
            'posicion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Delantero, Defensa'}),
        }

    def clean_nombre(self):
        raw_nombre = self.data.get('nombre')
        if raw_nombre is not None and not isinstance(raw_nombre, str):
            raise forms.ValidationError('Debe ser un texto.')
        nombre = (self.cleaned_data.get('nombre') or '').strip()
        if nombre and not nombre.replace(' ', '').isalpha():
            raise forms.ValidationError('El nombre solo debe contener letras.')
        return nombre

    def clean_apellido(self):
        raw_apellido = self.data.get('apellido')
        if raw_apellido is not None and not isinstance(raw_apellido, str):
            raise forms.ValidationError('Debe ser un texto.')
        apellido = (self.cleaned_data.get('apellido') or '').strip()
        if apellido and not apellido.replace(' ', '').isalpha():
            raise forms.ValidationError('El apellido solo debe contener letras.')
        return apellido

    def clean_posicion(self):
        raw_posicion = self.data.get('posicion')
        if raw_posicion is not None and not isinstance(raw_posicion, str):
            raise forms.ValidationError('Debe ser un texto.')
        posicion = (self.cleaned_data.get('posicion') or '').strip()
        if posicion and not posicion.replace(' ', '').isalpha():
            raise forms.ValidationError('La posición solo debe contener letras.')
        return posicion


class JugadorAPIForm(JugadorForm):
    def clean(self):
        cleaned_data = super().clean()
        edad = self.data.get('edad')
        if edad is not None and type(edad) is not int:
            self.add_error('edad', 'Debe ser un numero entero en JSON.')

        extra_fields = set(self.data) - set(self.fields)
        if extra_fields:
            self.add_error(None, 'Campos no permitidos: ' + ', '.join(sorted(extra_fields)))

        return cleaned_data