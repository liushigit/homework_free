from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.models import AnonymousUser
from rest_framework import exceptions

class GuestAuthentication(BaseAuthentication):

    def authenticate(self, request):
        # !!!Note: Don't call request.user(property) here, since that property also
        # calls this athenticate() method.
        print 'auth..'

        if request.method in ('OPTIONS'):
            return None

        if request.method in ('GET', 'PUT', 'DELETE', 'POST'):
            
            dj_request = getattr(request, '_request', None)
            if dj_request and hasattr(dj_request, 'user'):
                print "user: ", dj_request.user
                return (dj_request.user, None)

            print 'use token'
            token = request.META.get('HTTP_AUTHORIZATION')

            if token:
                from rest_framework.authtoken.models import Token
                
                token = token[6:]
                try:
                    print 'hit db'
                    t = Token.objects.get(key = token)
                    return (t.user, None)
                except Token.DoesNotExist:
                    raise exceptions.AuthenticationFailed('No such user')

        return None
