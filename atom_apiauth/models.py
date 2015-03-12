from django.db import models
from django.contrib.auth.models import User

class APIAuth(models.Model):
    user = models.ForeignKey(User)
    access_key = models.CharField(max_length=256)
