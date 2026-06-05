from django.http import HttpResponse

class HealthCheckMiddleware:
    def __init__(self, get_respone):
        self.get_response = get_respone

    def __call__(self, request):
        if request.path == '/health':
            return HttpResponse('ok')
        
        return self.get_response(request)