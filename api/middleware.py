from django.conf import settings
from django.http import HttpResponseForbidden
from rest_framework import status

class TokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.META.get('HTTP_AUTHORIZATION') == 'Token ' + settings.API_TOKEN:
            return HttpResponseForbidden('Invalid API token')
        response = self.get_response(request)
        
        return response
        
