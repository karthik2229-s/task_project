from django.contrib.auth.models import User
from django.db import models
import datetime

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    creator = models.ForeignKey(User, related_name='created_tasks', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, related_name='assigned_tasks', on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=50,choices=(('Assigned','Assigned'),('Closed','Closed')),default='Assigned')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True,null=True)
    last_updated_by = models.ForeignKey(User, related_name='updated_tasks', on_delete=models.SET_NULL, null=True, blank=True)