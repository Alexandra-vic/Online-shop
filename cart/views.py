from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from decimal import Decimal
from products.models import Product, CartItem
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    form = CartAddProductForm(request.POST)
    print(form.is_valid())
    for field in form:
        print("Field Error:", field.name,  field.errors)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            update_quantity=cd['update']
        )
        
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    print(cart)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    # for item in cart:
    #     item['price'] = Decimal(item['price'])
    #     item['quantity'] = 0 
    #     item['total_price'] = item['price'] * item['quantity']
    #     item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    # for item in cart:
    #     item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    print(cart)
    return render(request, 'cart.html', {'cart': cart})