from django.db import models
from django.urls import reverse
from cloudinary.models import CloudinaryField

# LABEL_CHOICES includes new options
LABEL_CHOICES = (
    ('P', 'Popular'),
    ('S', 'Special Offer'),
    ('D', 'New'),
    ('O', 'Out of Stock'),
    ('L', 'Low Stock'),
    ('N', 'None')  # Default: No label
)


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, db_index=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('list-category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = CloudinaryField('image')
    label = models.CharField(choices=LABEL_CHOICES, max_length=1, default='N')
    stock = models.PositiveIntegerField(default=0)  # Field to manage inventory

    class Meta:
        verbose_name_plural = 'products'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product-info', args=[self.slug])

    # Automatically set label based on stock
    def save(self, *args, **kwargs):
        stock_value = int(self.stock or 0)  # Ensure the stock value is treated as an integer
        if stock_value == 0:
            self.label = 'O'  # Out of Stock
        elif stock_value <= 5:
            # Low Stock only if not "Popular", "Special Offer", or "New"
            if self.label not in ['P', 'S', 'D']:
                self.label = 'L'
        else:
            # Reset label to None for sufficient stock if current label is "Out of Stock" or "Low Stock"
            if self.label in ['O', 'L']:
                self.label = 'N'

        super().save(*args, **kwargs)