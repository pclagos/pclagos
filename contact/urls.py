from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.contact, name='contact'),
    path('history/', views.service_history, name='service_history'),
    path('chat/<str:service_code>/', views.service_chat, name='service_chat'),
    path('chat/<str:service_code>/send/', views.send_message_ajax, name='send_message_ajax'),
    path('chat/<str:service_code>/messages/', views.get_messages_ajax, name='get_messages_ajax'),
    # Admin chat
    path('adminchat/', views.admin_chat_list, name='admin_chat_list'),
    path('adminchat/<str:service_code>/', views.admin_chat_detail, name='admin_chat_detail'),
] 