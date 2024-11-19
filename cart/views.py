from django.shortcuts import render
from .cart import Cart
from store.models import Product
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
# Create your views here.


def cart_summary(request):
    cart = Cart(request)
    return render(request, 'cart/cart-summary.html', {'cart':cart})

def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        print("Request POST data:", request.POST)  # Log incoming POST data

        product_id = request.POST.get('product_id')
        product_quantity = request.POST.get('product_quantity')

        # Validate product_id and product_quantity
        if not product_id or not product_quantity:
            return JsonResponse({'error': 'Product ID and quantity are required.'}, status=400)

        try:
            product_id = int(product_id)
            product_quantity = int(product_quantity)
        except ValueError:
            return JsonResponse({'error': 'Invalid product ID or quantity.'}, status=400)

        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, product_qty=product_quantity)
        cart_quantity = cart.__len__()

        return JsonResponse({'qty': cart_quantity})

    return JsonResponse({'error': 'Invalid request.'}, status=400)

   

def cart_delete(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':


        product_id = int(request.POST.get('product_id'))

        cart.delete(product = product_id)
        cart_quantity = cart.__len__()
        cart_total = cart.get_total()
        response = JsonResponse({'qty':cart_quantity, 'total':cart_total})
        return response

from django.http import JsonResponse
from .cart import Cart

def cart_update(request):
    cart = Cart(request)

    if request.method == 'POST' and request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        product_quantity = request.POST.get('product_quantity')

        # Validate product_id and product_quantity
        if not product_id or not product_quantity:
            return JsonResponse({'error': 'Product ID and quantity are required.'}, status=400)
        
        try:
            product_id = int(product_id)
            product_quantity = int(product_quantity)
        except ValueError:
            return JsonResponse({'error': 'Invalid product ID or quantity.'}, status=400)

        # Update the cart
        cart.update(product=product_id, qty=product_quantity)
        cart_quantity = len(cart.cart)  # or cart.__len__()
        cart_total = cart.get_total()

        response = JsonResponse({'qty': cart_quantity, 'total': cart_total})
        return response

    return JsonResponse({'error': 'Invalid request method.'}, status=400)


