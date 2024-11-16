from django.shortcuts import render

# Create your views here.

def checkout(request):
    return render(request, 'payment/checkout.html')
 

def payment_success(request):
    pass


def payment_failed(request):
    pass


