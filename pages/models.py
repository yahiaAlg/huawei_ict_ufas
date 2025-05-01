from django.db import models
from datetime import timezone
from django.contrib.auth.models import User

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    is_rtl = models.BooleanField(default=False)  # For right-to-left text direction
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-date']  # Most recent first


class GalleryImage(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='gallery/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_contacts')
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.email} - {self.created_at.strftime('%Y-%m-%d')}"
    
    def resolve(self, user):
        self.is_resolved = True
        self.resolved_by = user
        self.resolved_at = timezone.now()
        self.save()
    
    class Meta:
        ordering = ['-created_at']