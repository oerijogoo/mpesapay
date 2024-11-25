# payment/forms.py
from django import forms
from . models import  ShippingAddress

class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['full_name', 'address1', 'address2', 'city', 'state_name', 'zipcode']


        exclude = ['user',]

