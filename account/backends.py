from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.conf import settings
from django.db.models.signals import pre_save

from registration import signals
from registration.views import RegistrationView as BaseRegistrationView
from .forms import UserRegForm
#from account.models import UserProfile

def user_create_handler(sender, **kwargs):
    u = kwargs['instance']
    if not u.pk:
        u.is_active = False

pre_save.connect(user_create_handler, sender=User, dispatch_uid="registering")

class RegView(BaseRegistrationView):
    disallowed_url = 'account:registration_disallowed'
    template_name = 'registration/registration_form.html'
    
    def register(self, request, **cleaned_data):
        username, email, password = cleaned_data['username'], \
                                    cleaned_data['email'], \
                                    cleaned_data['password1']

        User.objects.create_user(username, email, password)
        new_user = authenticate(username=username, password=password)
        
        #login(request, new_user)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user
    
    def registration_allowed(self, request):
        return getattr(settings, 'REGISTRATION_OPEN', True)
        
    def get_form_class(self, request):
        return UserRegForm
    
    def get_success_url(self, request, user):
        return 'account:registration_complete'

