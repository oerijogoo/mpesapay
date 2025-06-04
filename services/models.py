from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils.text import slugify


class SiteSetting(models.Model):
    site_name = models.CharField(max_length=100)
    logo = CloudinaryField('logo', folder='cleaning_service/logo/', blank=True, null=True)
    favicon = CloudinaryField('favicon', folder='cleaning_service/favicon/', blank=True, null=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    motto = models.CharField(max_length=200, blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    about_us = models.TextField(blank=True, null=True)
    meta_title = models.CharField(max_length=100, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.site_name


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    icon_class = models.CharField(max_length=50, blank=True, null=True,
                                  help_text="Font Awesome icon class (e.g., fas fa-broom)")

    class Meta:
        verbose_name_plural = "Service Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    short_description = models.TextField()
    description = models.TextField()
    featured_image = CloudinaryField('featured_image', folder='cleaning_service/services/')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ServiceImage(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image', folder='cleaning_service/service_images/')
    caption = models.CharField(max_length=200, blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.service.title}"


class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    client_title = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField()
    image = CloudinaryField('image', folder='cleaning_service/testimonials/', blank=True, null=True)
    rating = models.PositiveIntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Testimonial by {self.client_name}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"


class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question