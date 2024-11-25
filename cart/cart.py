# cart/cart.py
from decimal import Decimal
from store.models import Product


class Cart:
    def __init__(self, request):
        """Initialize the cart."""
        self.session = request.session
        cart = self.session.get('session_key')

        if cart is None:  # Create a new cart if none exists
            cart = {}
            self.session['session_key'] = cart

        self.cart = cart

    def add(self, product, product_qty):
        """Add a product to the cart or update its quantity."""
        product_id = str(product.id)  # Ensure product_id is a string
        product_price = product.get_discounted_price()

        if product_id in self.cart:
            # Update the quantity if product exists
            self.cart[product_id]['qty'] += product_qty
        else:
            # Add the product as a new item in the cart
            self.cart[product_id] = {'price': str(product_price), 'qty': product_qty}

        # Mark the session as modified to save changes
        self.session.modified = True

    def __len__(self):
        """Return the total quantity of items in the cart."""
        return sum(item['qty'] for item in self.cart.values())

    def __iter__(self):
        """Iterate over the items in the cart and fetch related products from the database."""
        all_products_id = self.cart.keys()
        products = Product.objects.filter(id__in=all_products_id)
        import copy
        cart = copy.deepcopy(self.cart)

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])  # Convert price to Decimal
            item['total_price'] = item['price'] * item['qty']  # Calculate total price per item
            yield item

    def get_total(self):
        """Calculate the total price for all items in the cart."""
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())

    def delete(self, product):
        """Remove a product from the cart."""
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True

    def update(self, product, qty):
        """Update the quantity of a product in the cart."""
        product_id = str(product)

        # Convert qty to integer to ensure proper handling
        try:
            product_quantity = int(qty)
        except ValueError:
            product_quantity = 0  # Handle invalid quantity

        if product_id in self.cart:
            self.cart[product_id]['qty'] = product_quantity
            self.session.modified = True

    def clear(self):
        """Clear all items from the cart."""
        self.cart = {}
        self.session['session_key'] = self.cart
        self.session.modified = True
