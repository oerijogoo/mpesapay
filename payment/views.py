# payment/views.py
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from cart.cart import Cart
from .forms import ShippingForm
from .models import ShippingAddress, Order, OrderItem
from decimal import Decimal

from store.models import Product  # Import Product model for stock updates

# Payment Success View
def payment_success(request):
    return HttpResponse("Payment Successful! Your order has been processed.")  # You can render a template instead.

# Payment Failed View
def payment_failed(request):
    return HttpResponse("Payment Failed! Please try again.")  # You can render a template instead.

# Checkout View
def checkout(request):
    cart = Cart(request)  # Get the cart instance
    shipping_address = None

    # Pre-fill form for authenticated users
    if request.user.is_authenticated:
        shipping_address = ShippingAddress.objects.filter(user=request.user).first()

    if request.method == 'POST':
        full_name = request.POST.get('name')
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state_name = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        payment_method = request.POST.get('payment_method')

        if not all([full_name, email, address1, city]):
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'payment/checkout.html', {'cart': cart})

        # Save or update the shipping address
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
            shipping_address = ShippingAddress.objects.create(
                full_name=full_name,
                address1=address1,
                address2=address2,
                city=city,
                state_name=state_name,
                zipcode=zipcode
            )

        # Validate stock availability
        for item in cart:
            product = item['product']
            quantity = item['qty']
            if product.stock < quantity:
                messages.error(
                    request,
                    f"Insufficient stock for {product.title}. Available: {product.stock}, Requested: {quantity}."
                )
                return render(request, 'payment/checkout.html', {'cart': cart})

        # Create the order
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            email=email,
            shipping_address=f"{address1}, {address2}, {city}, {state_name}, {zipcode}",
            amount_paid=cart.get_total(),
            payment_method=payment_method
        )

        # Process order items and update stock
        for item in cart:
            product = item['product']
            quantity = item['qty']
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=item['price']
            )
            # Reduce stock
            product.stock -= quantity
            product.save()

        # Clear the cart
        cart.clear()

        # Redirect to success page
        messages.success(request, "Your order has been placed successfully!")
        return redirect('payment-success')

    return render(request, 'payment/checkout.html', {'cart': cart, 'form': ShippingForm(instance=shipping_address)})