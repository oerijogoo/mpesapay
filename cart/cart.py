from decimal import Decimal
from store.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        # Initialize cart from session or create a new one
        cart = self.session.get('session_key')
        
        if cart is None:  # Check if cart is None
            cart = {}
            self.session['session_key'] = cart
        
        self.cart = cart  # Assign the cart to self.cart

    def add(self, product, product_qty):
        product_id = str(product.id)  # Ensure product_id is a string

        if product_id in self.cart:
            # Update quantity if product exists in the cart
            self.cart[product_id]['qty'] += product_qty
        else:
            # Add new product to the cart
            self.cart[product_id] = {'price': str(product.price), 'qty': product_qty}

        # Mark the session as modified to save changes
        self.session.modified = True

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())
    
    def __iter__(self):
        all_products_id = self.cart.keys()
        products = Product.objects.filter(id__in=all_products_id)
        import copy
        cart = copy.deepcopy(self.cart)
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price']) * item['qty']  # Ensure price is calculated correctly
            yield item

    def get_total(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())
    
    def delete(self, product):
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True

    def update(self, product, qty):
        product_id = str(product)
        
        # Convert qty to integer to avoid issues
        try:
            product_quantity = int(qty)
        except ValueError:
            product_quantity = 0  # Set to 0 or handle as needed

        if product_id in self.cart:
            self.cart[product_id]['qty'] = product_quantity
            self.session.modified = True

    def clear(self):
        """Clears the cart session."""
        self.cart = {}  # Empty the cart
        self.session['session_key'] = self.cart  # Reset the session cart
        self.session.modified = True  # Mark the session as modified