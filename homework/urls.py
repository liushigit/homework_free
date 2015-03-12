from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^hw/', include('homeworkapp.urls', namespace="homework")),

    url(r'^$', RedirectView.as_view(url='/hw/'), name="index"),

    url(r'^accounts/', include('account.urls', namespace="account")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^captcha/', include('captcha.urls')),

    # Adding login to the Browsable API: 
    # http://www.django-rest-framework.org/tutorial/4-authentication-and-permissions
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # http://www.django-rest-framework.org/api-guide/authentication
    url(r'^api-token-auth', 'rest_framework.authtoken.views.obtain_auth_token'),

    url(r'^api/v1/', include('api_i.urls', namespace="api_i")),

)


if settings.DEBUG:
	from django.conf.urls.static import static

	urlpatterns += static(settings.MEDIA_URL, 
						  document_root=settings.MEDIA_ROOT)