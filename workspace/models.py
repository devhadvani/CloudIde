from django.db import models

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    last_modified = models.DateTimeField(auto_now=True)
    img = models.ImageField(upload_to='blog_images/', null=True, blank=True)  # Store image in 'media/blog_images/'
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return self.title