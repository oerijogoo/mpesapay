# store/views.py
from django.shortcuts import get_object_or_404, render
from .models import Category, Product
# Create your views here.

def store(request):
    all_products = Product.objects.all()
    context = {'all_products': all_products}
    return render(request, 'store/store.html', context=context)


def categories(request):
    all_categories = Category.objects.all()

    return {'all_categories': all_categories}


def product_info(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)

    # Get the available range of quantities based on stock
    quantity_range = range(1, product.stock + 1) if product.stock > 0 else []

    context = {
        'product': product,
        'quantity_range': quantity_range,
    }

    return render(request, 'store/product-info.html', context=context)

def list_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)

    products = Product.objects.filter(category=category)

    return render(request, 'store/list-category.html', {'category':category, 'products':products})


from datetime import datetime
from django.shortcuts import render

def year(request):
    current_year = datetime.now().year  # Get the current year
    return render(request, 'store/base.html', {'current_year': current_year})