# landscaping_app/models.py

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from cloudinary.models import CloudinaryField

class SiteSetting(models.Model):
    business_name = models.CharField(max_length=100)
    logo = CloudinaryField('logo', folder='landscaping/logos')
    motto = models.CharField(max_length=200, blank=True)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    about_us = models.TextField()
    google_maps_embed = models.TextField(help_text="Embed code for Google Maps")

    def __str__(self):
        return self.business_name

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class")
    featured_image = CloudinaryField('service_images', folder='landscaping/services')
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=100)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    description = models.TextField()
    before_image = CloudinaryField('project_images', folder='landscaping/projects/before')
    after_image = CloudinaryField('project_images', folder='landscaping/projects/after')
    date_completed = models.DateField()
    display_on_homepage = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    client_title = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    photo = CloudinaryField('testimonial_photos', folder='landscaping/testimonials', blank=True)
    display_on_homepage = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Testimonial from {self.client_name}"

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    photo = CloudinaryField('team_photos', folder='landscaping/team')
    display_order = models.PositiveIntegerField(default=0)
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"{self.name} - {self.position}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"