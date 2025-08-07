from django.db import models

# Create your models here.

class WorkGallery(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título del trabajo")
    description = models.TextField(verbose_name="Descripción del trabajo realizado")
    image = models.ImageField(upload_to='gallery/', verbose_name="Imagen del trabajo")
    service_type = models.CharField(max_length=100, verbose_name="Tipo de servicio")
    completed_date = models.DateField(verbose_name="Fecha de finalización")
    is_featured = models.BooleanField(default=False, verbose_name="Trabajo destacado")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de publicación")

    class Meta:
        verbose_name = "Trabajo en galería"
        verbose_name_plural = "Trabajos en galería"
        ordering = ['-completed_date']

    def __str__(self):
        return self.title
