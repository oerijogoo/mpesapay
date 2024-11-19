
from django.shortcuts import render, redirect
from django.contrib import messages
from cart.cart import Cart
from .models import ShippingAddress, Order, OrderItem



# Create your views here.


def checkout(request):
    cart = Cart(request)  # Get the cart instance

    if request.method == 'POST':
        # Get form data
        full_name = request.POST.get('name')
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state_name = request.POST.get('state')
        zipcode = request.POST.get('zipcode')

        # Validate required fields
        if not all([full_name, email, address1, city]):
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'payment/checkout.html', {'cart': cart})

        # Create or update shipping address for authenticated users
        if request.user.is_authenticated:
            shipping_address, created = ShippingAddress.objects.update_or_create(
                user=request.user,
                defaults={
                    'full_name': full_name,
                    'address1': address1,
                    'address2': address2,
                    'city': city,
                    'state_name': state_name,
                    'zipcode': zipcode,
                }
            )
        else:
            # Create temporary shipping address for anonymous users
            shipping_address = ShippingAddress.objects.create(
                full_name=full_name,
                address1=address1,
                address2=address2,
                city=city,
                state_name=state_name,
                zipcode=zipcode
            )

        # Create an order
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            email=email,
            shipping_address=f"{address1}, {address2}, {city}, {state_name}, {zipcode}",
            amount_paid=cart.get_total()
        )

        # Add items to the order
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['qty'],
                price=item['price']
            )

        # Clear the cart after order completion
        cart.clear()

        # Redirect to order success page
        messages.success(request, "Your order has been placed successfully!")
        return redirect('payment-success')  # Replace with the name of your success URL

    return render(request, 'payment/checkout.html', {'cart': cart})
 

def payment_success(request):
    return  render(request, 'payment/payment-success.html')


def payment_failed(request):
    pass


