from django.contrib import admin
from .models import WorkGallery

@admin.register(WorkGallery)
class WorkGalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'service_type', 'completed_date', 'is_featured']
    list_filter = ['is_featured', 'completed_date', 'created_at']
    search_fields = ['title', 'description', 'service_type']
    list_editable = ['is_featured']
    readonly_fields = ['created_at']
