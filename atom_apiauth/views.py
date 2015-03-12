from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .models import APIAuth
import string
import random

def _generate_key(size=128, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def _get_token(request, username, password):
    
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        try:
            return APIAuth.objects.get(user=user).access_key
        except:
            pass
        
        access_key = _generate_key()
        user_auth = APIAuth()
        user_auth.user = user
        user_auth.access_key = access_key
        user_auth.save()

        return access_key
        
def api_login(request):
    try:
        user = request.POST['username']
        password = request.POST['password']
        
        token = _get_token(request, user, password)
    except:
        token = None
        
    response = HttpResponse()
    
    if token:
        response['API-KEY'] = token
    else:
        response.status_code = 400
        response.content = 'Wrong combination of username and password'

    return response

