from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services_list, name='services'),
    path('gallery/', RedirectView.as_view(url='/contact/history/', permanent=True), name='gallery'),
] 