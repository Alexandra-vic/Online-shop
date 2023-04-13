from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic import TemplateView, FormView

# from django.contrib.auth import login

# from django.contrib.auth.decorators import login_required

from products.models import Category, Product, Cart, CartItem

from products.forms import CategoryForm, ProductForm

from cart.forms import CartAddProductForm


# def get_home_page(request):
    
#     return render(request, 'index.html')

class ProductListView(TemplateView):
    template_name = 'index.html'
    all_products = Product.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'products': Product.objects.all(),
            'categories': Category.objects.all(),
        })
        return context 
    
    def add_to_cart(request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart, _ = Cart.objects.get_or_create(pk=request.session.get('cart_id'))
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        request.session['cart_id'] = cart.pk
        return redirect('cart')

def cart(request):
    # cart = Cart.objects.get(pk=request.session.get('cart_id'))
    try:
        cart = Cart.objects.get(pk=request.session.get('cart_id'))
    except Cart.DoesNotExist:
        cart = None
    return render(request, 'cart.html', {'cart': cart})

class CategoryView(TemplateView):
    template_name = 'category.html'
    all_category = Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'categories': Category.objects.all(),
        })
        return context


class CategoryCreateView(TemplateView):
    template_name = 'category_create.html'

    def get(self, request):
        form = CategoryForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        if request.POST:
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save() 
                return redirect('category')  
        context = {'form': form, 'data': request.POST}
        return render(request, self.template_name, context)


class CategoryUpdateView(TemplateView):
    template_name = 'cat_update.html'

    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(instance=category)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category')
        context = {'form': form}
        return render(request, self.template_name, context)


class CategoryDeleteView(TemplateView):
    template_name = 'category_delete.html'

    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        context = {'category': category}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return redirect('category')


class ProductView(TemplateView):
    template_name = 'cart.html'
    all_products = Product.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'products': Product.objects.all(),
            'categories': Category.objects.all(),
        })
        return context    


class ProductAllView(TemplateView):
    template_name = 'product.html'
    all_products = Product.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'products': Product.objects.all(),
            'categories': Category.objects.all(),
        })
        return context          
    

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    cart_product_form = CartAddProductForm()
    return render(
        request, 'cart.html', {'product': product,'cart_product_form': cart_product_form})


class ProductCreateView(TemplateView):
    template_name = 'product_create.html'

    def get(self, request):
        form = ProductForm()
        categories = Category.objects.all() 
        return render(request, self.template_name, {'form': form, 'categories': categories})
    
    def post(self, request):
        if request.POST:
            form = ProductForm(request.POST)
            if form.is_valid():
                form.save() 
                return redirect('home') 
        categories = Category.objects.all()        
        context = {'form': form, 'categories': categories, 'data': request.POST}
        return render(request, self.template_name, context)
    

class ProductDeleteView(TemplateView):
    template_name = 'product_delete.html'

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        context = {'product': product}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return redirect('home')    
    

class ProductUpdateView(TemplateView):
    template_name = 'product_update.html'

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(instance=product)
        categories = Category.objects.all() 
        context = {'form': form, 'categories': categories, 'product': product}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product')
        context = {'form': form, 'product': product}
        return render(request, self.template_name, context)

   
# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = UserCreationForm()
#     return render(request, 'register.html', {'form': form})


# def add_to_cart(request):
#     form = AddToCartForm(request.POST)

#     if form.is_valid():
#         form.add_to_cart(request)
#         messages.success(request, 'Товар добавлен в корзину')
#     else:
#         messages.error(request, 'Не удалось добавить товар в корзину')

#     return redirect('basket.html', product_id=form.cleaned_data['product_id'])


# def view_cart(request):
#     cart_items = CartItem.objects.filter(user=request.user)

#     return render(request, 'basket.html', {'cart_items': cart_items})
