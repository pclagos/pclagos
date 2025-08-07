from django.shortcuts import render
from services.models import Service
from gallery.models import WorkGallery

# Create your views here.

def home(request):
    """Vista de la página principal"""
    services = Service.objects.filter(is_active=True)[:6]
    featured_works = WorkGallery.objects.filter(is_featured=True)[:3]
    context = {
        'services': services,
        'featured_works': featured_works,
    }
    return render(request, 'core/home.html', context)

def about(request):
    """Vista de la página Acerca de"""
    return render(request, 'core/about.html')

def services_list(request):
    """Vista de la lista de servicios"""
    services = Service.objects.filter(is_active=True)
    context = {
        'services': services,
    }
    return render(request, 'core/services.html', context)

def gallery(request):
    """Vista de la galería de trabajos"""
    works = WorkGallery.objects.all()
    context = {
        'works': works,
    }
    return render(request, 'core/gallery.html', context)
