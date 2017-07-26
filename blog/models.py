from django.db import models
from django.utils import timezone as tz


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    date_created = models.DateTimeField(default=tz.now)
    date_published = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.date_published = tz.now()
        self.save()

    def __str__(self):
        return self.title

    def approved_comments(self):
        return self.comments.filter(is_approved=True)

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    date_created = models.DateTimeField(default=tz.now)
    is_approved = models.BooleanField(default=False)

    def approve(self):
        self.is_approved=True
        self.save()
    def __str__(self):
        return self.text
