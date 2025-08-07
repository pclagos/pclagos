from django.contrib import admin
from .models import Contact, ServiceMessage, ServiceNote

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'service_code', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'phone', 'service_code', 'description']
    readonly_fields = ['service_code', 'created_at', 'qr_code']
    fields = ['name', 'email', 'phone', 'service_needed', 'description', 'service_code', 'status', 'qr_code', 'created_at', 'updated_at', 'notes']
    ordering = ['-created_at']

@admin.register(ServiceMessage)
class ServiceMessageAdmin(admin.ModelAdmin):
    list_display = ['contact', 'is_from_admin', 'message', 'created_at']
    list_filter = ['is_from_admin', 'created_at']
    search_fields = ['contact__service_code', 'message']
    readonly_fields = ['created_at']
    ordering = ['-created_at']

@admin.register(ServiceNote)
class ServiceNoteAdmin(admin.ModelAdmin):
    list_display = ['contact', 'note', 'manual_date', 'created_at']
    list_filter = ['created_at', 'manual_date']
    search_fields = ['contact__service_code', 'note']
    readonly_fields = ['created_at']
    fields = ['contact', 'note', 'manual_date', 'created_at']
    ordering = ['-created_at']
