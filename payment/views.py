from django.shortcuts import render, redirect
from django.contrib import messages
from cart.cart import Cart
from .models import ShippingAddress, Order, OrderItem
from .forms import ShippingForm


def checkout(request):
    cart = Cart(request)  # Get the cart instance

    # Prepopulate form for authenticated users
    initial_data = {}
    if request.user.is_authenticated:
        try:
            user_shipping = ShippingAddress.objects.filter(user=request.user).first()
            if user_shipping:
                initial_data = {
                    'full_name': user_shipping.full_name,
                    'address1': user_shipping.address1,
                    'address2': user_shipping.address2,
                    'city': user_shipping.city,
                    'state_name': user_shipping.state_name,
                    'zipcode': user_shipping.zipcode,
                }
        except ShippingAddress.DoesNotExist:
            initial_data = {
                'full_name': request.user.get_full_name(),
                'email': request.user.email,
            }

    shipping_form = ShippingForm(initial=initial_data)

    if request.method == 'POST':
        shipping_form = ShippingForm(request.POST)
        if shipping_form.is_valid():
            # Save or update the shipping address
            shipping_address = shipping_form.save(commit=False)
            if request.user.is_authenticated:
                shipping_address.user = request.user
            shipping_address.save()

            # Create an order
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                full_name=shipping_form.cleaned_data['full_name'],
                email=request.POST.get('email'),  # Manually fetch email from the POST request
                shipping_address=f"{shipping_form.cleaned_data['address1']}, {shipping_form.cleaned_data['address2']}, "
                                 f"{shipping_form.cleaned_data['city']}, {shipping_form.cleaned_data['state_name']}, "
                                 f"{shipping_form.cleaned_data['zipcode']}",
                amount_paid=cart.get_total()
            )

            # Add items to the order and reduce product stock
            for item in cart:
                product = item['product']
                quantity = item['qty']

                if product.stock >= quantity:
                    product.stock -= quantity
                    product.save()
                else:
                    messages.error(request, f"Not enough stock for {product.title}.")
                    return redirect("store")

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=item['price']
                )

            # Store the paid amount in session
            request.session['paid_amount'] = float(cart.get_total())

            # Clear the cart after order completion
            cart.clear()

            messages.success(request, "Your order has been placed successfully!")
            return redirect('payment-success')  # Replace with your success page URL
        else:
            messages.error(request, "Please correct the errors in the form.")

    return render(request, 'payment/checkout.html', {
        'shipping_form': shipping_form,
        'cart': cart,
        'total': cart.get_total(),
    })


def payment_success(request):
    paid_amount = request.session.get('paid_amount', 0)  # Default to 0 if not set
    return render(request, 'payment/payment-success.html', {'paid_amount': paid_amount})



def payment_failed(request):
    pass