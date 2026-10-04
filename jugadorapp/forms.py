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