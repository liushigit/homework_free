from rest_framework import serializers
from homeworkapp.models import Course, Assignment, Submission, Attachment

class CourseSerializer(serializers.ModelSerializer):
	# assignment_set = serializers.RelatedField(many=True)
	class Meta:
		model = Course
		fields = ('id', 'created', 'name', 'slug', 'archived', 'assignment_set')


class AssignmentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Assignment
		fields = ('id', 'title', )


class AssignmentDetailSerializer(serializers.ModelSerializer):

	class Meta:
		model = Assignment
		fields = ('id', 'title', 'description', 
			      'course', 'due_date', 'attachment_set')
		read_only_fields = ('attachment_set',)
