from django.db import models
import random
import string
import qrcode
from io import BytesIO
from django.core.files import File
from django.urls import reverse
from django.conf import settings

def generate_service_code():
    """Genera un código de servicio único tipo TY001"""
    # Excluir la letra O para evitar confusión con el número 0
    available_letters = string.ascii_uppercase.replace('O', '')
    letters = ''.join(random.choices(available_letters, k=2))
    
    # Buscar el último número usado (solo el número, las letras son aleatorias)
    last_contact = Contact.objects.order_by('-service_code').first()
    if last_contact and last_contact.service_code:
        try:
            last_number = int(last_contact.service_code[2:])
            new_number = last_number + 1
            # Si llegamos al 1000, reiniciar a 1
            if new_number > 1000:
                new_number = 1
        except ValueError:
            new_number = 1
    else:
        new_number = 1
    
    # Formatear con 3 dígitos para números 1-999, 4 dígitos para 1000
    if new_number == 1000:
        return f"{letters}{new_number}"
    else:
        return f"{letters}{new_number:03d}"

class Contact(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('in_progress', 'En Progreso'),
        ('completed', 'Completado'),
        ('cancelled', 'Cancelado'),
    ]

    name = models.CharField(max_length=100, verbose_name="Nombre")
    email = models.EmailField(verbose_name="Correo electrónico")
    phone = models.CharField(max_length=20, verbose_name="Teléfono")
    service_needed = models.CharField(max_length=200, verbose_name="Servicio requerido")
    description = models.TextField(verbose_name="Descripción del problema")
    service_code = models.CharField(max_length=6, unique=True, verbose_name="Código de servicio")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Estado")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de solicitud")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    notes = models.TextField(blank=True, null=True, verbose_name="Notas del técnico")
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True, verbose_name="Código QR")

    class Meta:
        verbose_name = "Solicitud de contacto"
        verbose_name_plural = "Solicitudes de contacto"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.service_code} - {self.name} - {self.service_needed}"
    
    def get_chat_url(self):
        """Retorna la URL completa del chat del servicio"""
        return f"{settings.SITE_URL}{reverse('contact:service_chat', kwargs={'service_code': self.service_code})}"
    
    def generate_qr_code(self):
        """Genera un código QR con la URL del chat"""
        if not self.qr_code:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(self.get_chat_url())
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            
            filename = f'qr_{self.service_code}.png'
            self.qr_code.save(filename, File(buffer), save=False)
            buffer.close()
    
    def save(self, *args, **kwargs):
        # Generar código QR si no existe
        if not self.qr_code:
            super().save(*args, **kwargs)
            self.generate_qr_code()
        super().save(*args, **kwargs)

class ServiceMessage(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='messages', verbose_name="Contacto")
    message = models.TextField(verbose_name="Mensaje")
    is_from_admin = models.BooleanField(default=False, verbose_name="Es del administrador")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        ordering = ['created_at']
        verbose_name = "Mensaje de servicio"
        verbose_name_plural = "Mensajes de servicio"

    def __str__(self):
        return f"{self.contact.service_code} - {'Admin' if self.is_from_admin else 'Cliente'} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"

class ServiceNote(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='service_notes', verbose_name="Contacto")
    note = models.TextField(verbose_name="Nota")
    manual_date = models.DateTimeField(verbose_name="Fecha manual", null=True, blank=True, help_text="Fecha que se mostrará al usuario (dejar vacío para usar fecha automática)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Nota de servicio"
        verbose_name_plural = "Notas de servicio"

    def __str__(self):
        return f"{self.contact.service_code} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"
    
    @property
    def display_date(self):
        """Retorna la fecha manual si existe, sino la fecha de creación"""
        return self.manual_date if self.manual_date else self.created_at
