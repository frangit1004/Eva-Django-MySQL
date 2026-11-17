from django import forms
from .models import Jugador


class JugadorForm(forms.ModelForm):
    nombre = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del jugador'}),
        error_messages={
            'required': 'El nombre es obligatorio.',
            'max_length': 'El nombre no puede superar los 20 caracteres.',
        },
    )
    apellido = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido del jugador'}),
        error_messages={
            'required': 'El apellido es obligatorio.',
            'max_length': 'El apellido no puede superar los 20 caracteres.',
        },
    )
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
    posicion = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Delantero, Defensa'}),
        error_messages={
            'required': 'La posición es obligatoria.',
            'max_length': 'La posición no puede superar los 50 caracteres.',
        },
    )

    class Meta:
        model = Jugador
        fields = ['nombre', 'apellido', 'edad', 'posicion']

    def clean_nombre(self):
        raw_nombre = self.data.get('nombre')
        if raw_nombre is not None and not isinstance(raw_nombre, str):
            raise forms.ValidationError('El nombre debe ser una cadena de texto.')
        nombre = (self.cleaned_data.get('nombre') or '').strip()
        if not nombre:
            raise forms.ValidationError('El nombre no puede estar vacío.')
        if not nombre.replace(' ', '').isalpha():
            raise forms.ValidationError('El nombre solo debe contener letras.')
        return nombre

    def clean_apellido(self):
        raw_apellido = self.data.get('apellido')
        if raw_apellido is not None and not isinstance(raw_apellido, str):
            raise forms.ValidationError('El apellido debe ser una cadena de texto.')
        apellido = (self.cleaned_data.get('apellido') or '').strip()
        if not apellido:
            raise forms.ValidationError('El apellido no puede estar vacío.')
        if not apellido.replace(' ', '').isalpha():
            raise forms.ValidationError('El apellido solo debe contener letras.')
        return apellido

    def clean_posicion(self):
        raw_posicion = self.data.get('posicion')
        if raw_posicion is not None and not isinstance(raw_posicion, str):
            raise forms.ValidationError('La posición debe ser una cadena de texto.')
        posicion = (self.cleaned_data.get('posicion') or '').strip()
        if not posicion:
            raise forms.ValidationError('La posición no puede estar vacía.')
        if not posicion.replace(' ', '').isalpha():
            raise forms.ValidationError('La posición solo debe contener letras.')
        return posicion


class JugadorAPIForm(JugadorForm):
    def clean(self):
        cleaned_data = super().clean()
        edad = self.data.get('edad')
        if edad is not None and (isinstance(edad, bool) or not isinstance(edad, int)):
            self.add_error('edad', 'La edad debe ser un número entero válido.')

        extra_fields = set(self.data.keys()) - set(self.fields.keys())
        if extra_fields:
            self.add_error(None, 'Campos no permitidos: ' + ', '.join(sorted(extra_fields)))

        return cleaned_data