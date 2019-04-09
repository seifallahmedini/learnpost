from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    event_datetime = models.DateTimeField()
    duration = models.IntegerField()
    theme = models.CharField(max_length=20)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name="event_likes")
    instructors = models.ManyToManyField(User, blank=True, related_name="event_instructors")

    def __str__(self):
        return self.title