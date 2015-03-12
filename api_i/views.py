from django.db.models import Count

from .serializers import (CourseSerializer, 
						  AssignmentSerializer, 
						  AssignmentDetailSerializer)
from homeworkapp.models import Course, Assignment, Submission, Attachment
from .auth import GuestAuthentication

from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response

from rest_framework.permissions import IsAdminUser


# http://www.django-rest-framework.org/api-guide/viewsets

class CourseListAPI(viewsets.ModelViewSet):
	"""
    The active course list for teachers.
	"""
	queryset = Course.objects.all()
	serializer_class = CourseSerializer
	authentication_classes = (GuestAuthentication, )

	resource_name = False

	permissions_classes = (IsAdminUser, )
	# paginate_by = 100

	def get_queryset(self):
		user = self.request.user
		
		# The Chrome browser doesn't send token with the OPTIONS method,
		# so user may be an AnonymousUser, which doesn't have a course_set.
		if hasattr(user, 'course_set'):
			return user.course_set.filter(archived=False)\
							  	  .annotate(n_assigns=Count('assignment'))
		else:
			return []


	def list(self, request):
		data = {'course': [], 'assignment': []}
		for course in self.get_queryset():
			course_serializer = CourseSerializer(course)
			data['course'].append(course_serializer.data)

			for assi in course.assignment_set.all():
				assi_serializer = AssignmentDetailSerializer(assi)
				data['assignment'].append(assi_serializer.data)
		
		return Response(data)

	def create(self, request):
		self.resource_name = 'course'
		course = Course(**request.DATA)
		course.user = request.user
		course.save()
		return Response('') # ?


class AssignmentViewSet(viewsets.ModelViewSet):
	queryset = Assignment.objects.all()
	serializer_class = AssignmentDetailSerializer

	def create(self, request, *args, **kwargs):
		ret = super(viewsets.ModelViewSet, self).create(request, *args, **kwargs)
		
		return ret
	

# class AssignmentAPI(generics.RetrieveUpdateDestroyAPIView):
# 	queryset = Assignment.objects.all()
# 	serializer_class = AssignmentSerializer


