from django.db import models
from django.contrib.auth.models import User
from general_tools_app.models.fields import MobileNumberField

class UserProfile(models.Model):
    user = models.OneToOneField(User, editable=False)
    real_name = models.CharField(max_length=30, editable=False)
    student_number = models.BigIntegerField(editable=False)
    phone = MobileNumberField(blank = True)

    def __unicode__(self):
        return self.user.username
