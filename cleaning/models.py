from django.db import models
from cloudinary.models import CloudinaryField
from django.utils.text import slugify

class SiteSetting(models.Model):
    site_name = models.CharField(max_length=100)
    logo = CloudinaryField('logo', folder='cleaning_service/logos')
    motto = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    about_us = models.TextField(blank=True)
    meta_title = models.CharField(max_length=100, blank=True)
    meta_description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    icon_class = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    description = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Service Categories"
        ordering = ['display_order']

class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    short_description = models.CharField(max_length=200)
    description = models.TextField()
    image = CloudinaryField('service_image', folder='cleaning_service/services')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.category.name}"

    class Meta:
        ordering = ['display_order']

class GalleryImage(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='gallery_images', blank=True, null=True)
    image = CloudinaryField('gallery_image', folder='cleaning_service/gallery')
    caption = models.CharField(max_length=200, blank=True)
    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.caption if self.caption else f"Image {self.id}"

class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    client_title = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    image = CloudinaryField('testimonial_image', folder='cleaning_service/testimonials', blank=True, null=True)
    rating = models.PositiveIntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"Testimonial from {self.client_name}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"

    class Meta:
        ordering = ['-created_at']