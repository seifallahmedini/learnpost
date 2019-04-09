from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    likes = models.ManyToManyField(User, blank=True, related_name="post_likes")
    main_question = models.TextField(default="This is the main question of the Post")
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to="posts_photos")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    def get_api_like_url(self):
        return reverse('like-api-toggle', kwargs={'pk': self.pk})

    def snippet(self):
        return str(self.content)[:100] + "..."


class Comment(models.Model):
    content = models.TextField()
    on_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User,default='', on_delete=models.CASCADE)

    def __str__(self):
        return self.content