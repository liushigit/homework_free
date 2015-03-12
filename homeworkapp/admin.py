from django.contrib import admin
from .models import Submission, Course, Assignment

class CourseAdmin(admin.ModelAdmin):
    list_display = [ 'created', 'name', 'slug', 'archived']


admin.site.register(Course, CourseAdmin)
admin.site.register(Assignment)
admin.site.register(Submission)