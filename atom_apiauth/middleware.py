from django.contrib.auth import login
from .models import APIAuth

class APIKeyAuthMiddleware:
    def process_request(self, request):
        try:
            token = request.META['API-KEY']
            if not token:
                token = request.GET['key']
            user = APIAuth.objects.get(access_key=token).user
            user.backend='django.contrib.auth.backends.ModelBackend'
            if user:
                login(request, user)
        except:
            pass


class TokenAuthMiddleware:
    def process_request(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')

        if token:
            from rest_framework.authtoken.models import Token
            
            token = token[6:]
            try:
                t = Token.objects.get(key = token)
                user = t.user
                user.backend='django.contrib.auth.backends.ModelBackend'
                login(request, user)

            except Token.DoesNotExist as e:
                pass


class AllowOriginMiddleware:

    def process_request(self, request):
        pass
    
    def process_response(self, req, res):
        res['Access-Control-Allow-Origin'] = '*'
        res['Access-Control-Allow-Headers'] = 'Content-Type, X-Forwarded-For, '\
                                              'Remote-Addr, '\
                                              'Accept, Origin, Authorization'
        res['Access-Control-Allow-Credentials'] = 'true'
        res['Access-Control-Max-Age'] = "1728000"
        res['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE, OPTIONS'
        return res

