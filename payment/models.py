# payment/models.py
from django.db import models
from django.contrib.auth.models import User

from store.models import Product


# Create your models here.


class ShippingAddress(models.Model):
    full_name = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state_name = models.CharField(max_length=255, null=True, blank=True)
    zipcode = models.CharField(max_length=255, null=True, blank=True)

    user= models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


    class Mata:
        verbose_name_plural = 'Shipping Address'


    def __str__(self):

        return 'Shipping Address - '+ str(self.id)
    

class Order(models.Model):
    PAYMENT_CHOICES = [
        ('CASH', 'Cash'),
        ('MPESA', 'M-Pesa'),
        ('BOTH', 'Cash & M-Pesa')
    ]
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    shipping_address = models.TextField(max_length=1000)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='CASH')
    date_orderd = models.DateTimeField(auto_now_add=True)

    user= models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return 'Order -#'+ str(self.id)

class OrderItem(models.Model):
    # ForeignKey to Order
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    
    # ForeignKey to Product
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    # ForeignKey to User (optional)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return 'Order -'+ str(self.id)


        

