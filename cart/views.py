
# cart/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from .cart import Cart
from store.models import Product

# Cart Summary
def cart_summary(request):
    cart = Cart(request)
    cart_items = []
    cart_total = 0

    for product_id, item in cart.cart.items():
        product = get_object_or_404(Product, id=product_id)
        discounted_price = product.get_discounted_price()
        total_price = discounted_price * item['qty']

        cart_items.append({
            'product': product,
            'quantity': item['qty'],
            'price': discounted_price,
            'total': total_price,
        })
        cart_total += total_price

    return render(request, 'cart/cart-summary.html', {'cart_items': cart_items, 'cart_total': cart_total})


# Add Product to Cart
def cart_add(request):
    cart = Cart(request)

    if request.method == 'POST' and request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        product_quantity = request.POST.get('product_quantity')

        # Validate product ID and quantity
        if not product_id or not product_quantity:
            return JsonResponse({'error': 'Product ID and quantity are required.'}, status=400)

        try:
            product_id = int(product_id)
            product_quantity = int(product_quantity)
        except ValueError:
            return JsonResponse({'error': 'Invalid product ID or quantity.'}, status=400)

        product = get_object_or_404(Product, id=product_id)

        # Check stock availability
        if product_quantity > product.stock:
            return JsonResponse({'error': 'Not enough stock available.'}, status=400)

        # Add to cart
        cart.add(product=product, product_qty=product_quantity)
        cart_quantity = cart.__len__()
        cart_total = cart.get_total()

        return JsonResponse({'qty': cart_quantity, 'total': cart_total})

    return JsonResponse({'error': 'Invalid request method.'}, status=400)


# Delete Product from Cart
def cart_delete(request):
    cart = Cart(request)

    if request.method == 'POST' and request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')

        try:
            product_id = int(product_id)
        except ValueError:
            return JsonResponse({'error': 'Invalid product ID.'}, status=400)

        cart.delete(product=product_id)
        cart_quantity = cart.__len__()
        cart_total = cart.get_total()

        return JsonResponse({'qty': cart_quantity, 'total': cart_total})

    return JsonResponse({'error': 'Invalid request method.'}, status=400)


# Update Product Quantity in Cart
def cart_update(request):
    cart = Cart(request)

    if request.method == 'POST' and request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        product_quantity = request.POST.get('product_quantity')

        # Validate product ID and quantity
        if not product_id or not product_quantity:
            return JsonResponse({'error': 'Product ID and quantity are required.'}, status=400)

        try:
            product_id = int(product_id)
            product_quantity = int(product_quantity)
        except ValueError:
            return JsonResponse({'error': 'Invalid product ID or quantity.'}, status=400)

        product = get_object_or_404(Product, id=product_id)

        # Check stock availability
        if product_quantity > product.stock:
            return JsonResponse({'error': 'Not enough stock available.'}, status=400)

        # Update cart
        cart.update(product=product_id, qty=product_quantity)
        cart_quantity = cart.__len__()
        cart_total = cart.get_total()

        return JsonResponse({'qty': cart_quantity, 'total': cart_total})

    return JsonResponse({'error': 'Invalid request method.'}, status=400)


# Checkout View
def checkout(request):
    cart = Cart(request)

    if not cart.__len__():
        return redirect('cart-summary')  # Redirect to cart if it's empty

    # Get the cart items and total cost
    cart_items = []
    cart_total = 0

    for product_id, item in cart.cart.items():
        product = get_object_or_404(Product, id=product_id)
        discounted_price = product.get_discounted_price()
        total_price = discounted_price * item['qty']

        cart_items.append({
            'product': product,
            'quantity': item['qty'],
            'price': discounted_price,
            'total': total_price,
        })
        cart_total += total_price

    # Handle form submission for checkout (e.g., shipping info)
    if request.method == 'POST':
        # Here you would normally capture shipping details and payment info
        name = request.POST.get('name')
        address = request.POST.get('address')

        if not name or not address:
            return HttpResponse("Please provide all required information.", status=400)

        # In real use, save order to the database, process payment, etc.
        # For now, we'll just clear the cart and confirm the order
        cart.clear()
        return render(request, 'cart/order-confirmation.html', {
            'cart_items': cart_items,
            'cart_total': cart_total,
            'name': name,
            'address': address
        })

    return render(request, 'cart/checkout.html', {
        'cart_items': cart_items,
        'cart_total': cart_total
    })
