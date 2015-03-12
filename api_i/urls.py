from django.conf.urls import patterns, include, url
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter(trailing_slash=False)
router.register(r'courses', views.CourseListAPI )
router.register(r'assignments', views.AssignmentViewSet )

urlpatterns = patterns('',
	url(r'^', include(router.urls) ),
	# url(r'^assignments/(?P<pk>[0-9]+)$', views.AssignmentAPI.as_view()),
)