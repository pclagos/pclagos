from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'service_needed', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tu@email.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu número de teléfono'}),
            'service_needed': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Reparación de laptop, Instalación de Windows, etc.'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe el problema que tienes con tu computadora...'}),
        }
        labels = {
            'name': 'Nombre completo',
            'email': 'Correo electrónico',
            'phone': 'Teléfono',
            'service_needed': 'Servicio requerido',
            'description': 'Descripción del problema',
        } 