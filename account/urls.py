from django.conf.urls import patterns, url
from account.backends import RegView
from django.views.generic.base import TemplateView
from .views import ChangePasswordView, ProfileUpdateView


urlpatterns = patterns ('', 
    url(r'^login$', 'django.contrib.auth.views.login', 
        {'template_name':'account/login.html'}, name="login"), 

    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name="logout"), 
    
    url(r'^changepass$', ChangePasswordView.as_view(), name="change-pass"), 
    
    url(r'^register$', RegView.as_view(), name='register'), 
    
    url(r'^profile/update$', ProfileUpdateView.as_view(), name='update-profile'), 
    
    url(r'^not-activated$',
        TemplateView.as_view(template_name='account/not_activated.html'),
            name='not-activated'),

    url(r'^register/closed$',
        TemplateView.as_view(template_name='registration/registration_closed.html'),
            name='registration_disallowed'),

    url(r'register/complete$', 
        TemplateView.as_view(template_name='registration/registration_complete.html'),
            name='registration_complete'),
        
    url(r'register/activated$', 
        TemplateView.as_view(template_name='registration/activation_complete.html'),
            name='activation_complete'),
)
