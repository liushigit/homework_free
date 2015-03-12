# coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from .storage import OverwriteStorage
import os.path as op

from datetime import datetime, time
from django.utils import timezone as djtz

def _submission_path(instance, filename):
    fn, ext = op.splitext(filename)
    course_bit = instance.assignment.course.slug
    assignment_bit = str(instance.assignment_id)
    user_bit = instance.user.username + ext
    
    return op.join(course_bit, assignment_bit, user_bit)

def attachment_path(instance, filename):
    course_bit = instance.assignment.course.slug
    assignment_bit = unicode(instance.assignment_id)
    return op.join(course_bit, 
                   assignment_bit, 'atta', 
                   filename)


class Course(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, editable = False)
    slug = models.SlugField(unique=True)
    students = models.ManyToManyField(
                User, 
                related_name='course_joined', 
                editable=False)

    archived = models.BooleanField(editable = False)

    def has_student(self, user_id):
        return self.students.filter(pk = user_id).exists()
        

class Assignment(models.Model):
    course = models.ForeignKey(Course)
    title = models.CharField(max_length=256)
    description = models.TextField(max_length=256)
    due_date = models.DateField()
    #user = models.ForeignKey(User, editable = False)
    
    @property
    def user(self):
        return self.course.user
    
    def has_user_submitted(self, user_id):
        return self.submission_set.filter(user_id = user_id).exists()
    
    @property
    def is_due(self):
        return self.due_datetime < djtz.now()
    
    @property
    def due_datetime(self):
        return datetime.combine(self.due_date, time.max).\
                        replace(tzinfo=djtz.get_default_timezone())
        
#    def time_left(self):
#        now = djtz.now()
#        return self.due_datetime - now

    class Meta:
        get_latest_by = "due_date"
        ordering = ['due_date']



class Submission(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    
    assignment = models.ForeignKey(Assignment, editable=False)
    user = models.ForeignKey(User, editable=False)

    file = models.FileField(upload_to = _submission_path, 
                            storage = OverwriteStorage(), 
                            blank = True)
    
    
class Attachment(models.Model):
    assignment = models.ForeignKey(Assignment, editable=False)

    file = models.FileField(upload_to = attachment_path, 
                            storage = OverwriteStorage())
    

