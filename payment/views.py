from django.shortcuts import render

from payment.models import ShippingAddress

# Create your views here.

def checkout(request):
    if request.user.is_authenticated:
        try:
            # Try to get the authenticated user's shipping address
            shipping_address = ShippingAddress.objects.get(user=request.user)
            context = {'shipping': shipping_address}
        except ShippingAddress.DoesNotExist:
            # If the user is authenticated but has no shipping address
            context = {'shipping': None}  # Or handle as needed
    else:
        # If the user is not authenticated
        context = {'shipping': None}  # Or handle as needed

    return render(request, 'payment/checkout.html', context)
 

def payment_success(request):
    pass


def payment_failed(request):
    pass


