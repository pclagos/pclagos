from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from .forms import ContactForm
from .models import Contact, ServiceMessage, ServiceNote
import random
import string
import os
from datetime import datetime

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

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                contact = form.save(commit=False)
                contact.service_code = generate_service_code()
                contact.save()
                ServiceMessage.objects.create(
                    contact=contact,
                    message=contact.description,
                    is_from_admin=False
                )
                request.session['service_code_message'] = contact.service_code
                return redirect('contact:service_history')
            except Exception as e:
                print(f"Error guardando contacto: {e}")
                messages.error(request, 'Hubo un error al procesar tu solicitud. Por favor intenta nuevamente.')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = ContactForm()
    context = {'form': form}
    return render(request, 'contact/contact.html', context)

def service_history(request):
    service_code_message = request.session.get('service_code_message', None)
    if request.method == 'POST':
        service_code = request.POST.get('service_code', '').strip().upper()
        try:
            contact = Contact.objects.get(service_code=service_code)
            return redirect('contact:service_chat', service_code=service_code)
        except Contact.DoesNotExist:
            messages.error(request, 'Código de servicio no encontrado. Verificá que esté correcto.')
    
    # Obtener el contacto si hay un código de servicio en la sesión
    contact = None
    if service_code_message:
        try:
            contact = Contact.objects.get(service_code=service_code_message)
        except Contact.DoesNotExist:
            pass
    
    return render(request, 'contact/service_history.html', {
        'service_code_message': service_code_message,
        'contact': contact
    })

def service_chat(request, service_code):
    contact = get_object_or_404(Contact, service_code=service_code)
    context = {
        'contact': contact,
        'messages': contact.messages.all(),
    }
    return render(request, 'contact/service_chat.html', context)

def send_message_ajax(request, service_code):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        contact = get_object_or_404(Contact, service_code=service_code)
        
        # Verificar si el servicio está completado o cancelado
        if contact.status == 'completed':
            return JsonResponse({'success': False, 'error': 'El servicio está completado y no se pueden enviar más mensajes.'})
        elif contact.status == 'cancelled':
            return JsonResponse({'success': False, 'error': 'El servicio está cancelado y no se pueden enviar más mensajes.'})
        
        message_text = request.POST.get('message', '').strip()
        is_admin = request.POST.get('is_admin', 'false') == 'true'
        if message_text:
            ServiceMessage.objects.create(
                contact=contact,
                message=message_text,
                is_from_admin=is_admin
            )
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def get_messages_ajax(request, service_code):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        contact = get_object_or_404(Contact, service_code=service_code)
        messages_qs = contact.messages.all()
        messages_list = [
            {
                'message': m.message,
                'is_from_admin': m.is_from_admin,
                'created_at': m.created_at.strftime('%d/%m/%Y %H:%M')
            }
            for m in messages_qs
        ]
        return JsonResponse({'messages': messages_list})
    return JsonResponse({'messages': []})

# Vista especial para admin
@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_chat_list(request):
    if request.method == 'POST':
        service_code = request.POST.get('service_code')
        status = request.POST.get('status')
        contact = Contact.objects.filter(service_code=service_code).first()
        if contact and status in dict(Contact.STATUS_CHOICES):
            contact.status = status
            contact.save()
    contacts = Contact.objects.all().order_by('-created_at')
    return render(request, 'contact/admin_chat_list.html', {'contacts': contacts})

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_chat_detail(request, service_code):
    contact = get_object_or_404(Contact, service_code=service_code)
    
    if request.method == 'POST':
        note_text = request.POST.get('note', '').strip()
        note_date = request.POST.get('note_date', '').strip()
        
        if note_text:
            # Procesar la fecha manual si se proporciona
            manual_date = None
            if note_date:
                try:
                    manual_date = datetime.fromisoformat(note_date.replace('T', ' '))
                    if timezone.is_naive(manual_date):
                        manual_date = timezone.make_aware(manual_date)
                except ValueError:
                    pass  # Si hay error en el formato, usar fecha automática
            
            ServiceNote.objects.create(
                contact=contact,
                note=note_text,
                manual_date=manual_date
            )
            messages.success(request, 'Nota agregada correctamente.')
            return redirect('contact:admin_chat_detail', service_code=service_code)
    
    # Formatear fecha actual para el input datetime-local
    current_datetime = timezone.now().strftime('%Y-%m-%dT%H:%M')
    
    context = {
        'contact': contact,
        'messages': contact.messages.all(),
        'notes': contact.service_notes.all(),
        'is_admin': True,
        'current_datetime': current_datetime,
    }
    return render(request, 'contact/admin_service_chat.html', context)
