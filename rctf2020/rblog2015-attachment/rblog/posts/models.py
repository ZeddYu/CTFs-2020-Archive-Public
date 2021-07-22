from django.db import models
from django.contrib.auth.models import User
import uuid


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)


class Feedback(models.Model):
    link = models.CharField(max_length=200)
    highlight_word = models.CharField(max_length=200)
    ip = models.GenericIPAddressField()
    create_at = models.DateTimeField(auto_now_add=True)
    is_viewed = models.BooleanField(default=False)
