from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import os

@csrf_exempt
@require_http_methods(["POST"])
def health_check(request):
    """Health check endpoint for Vercel"""
    return JsonResponse({
        'status': 'ok',
        'environment': os.environ.get('VERCEL_ENV', 'local'),
        'message': 'Django app is running'
    })
