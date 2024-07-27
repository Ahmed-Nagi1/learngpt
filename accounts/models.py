from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
import uuid



class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    stage = models.CharField(max_length=10, null=True, blank=True)
    is_sub = models.BooleanField(default=False)
    count = models.IntegerField(default=5)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
