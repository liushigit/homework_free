from django.conf.urls import patterns, url
from .views import api_login

#from django.views.decorators.cache import cache_page

urlpatterns = patterns('data_services.views', 
    url(r'^api_login$', api_login, name='api_login'), 
)

