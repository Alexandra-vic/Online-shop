from django import forms
from django.contrib.auth import get_user_model

from products.models import Category, Product, CartItem
from django.core.validators import RegexValidator


class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        max_length=60, 
        validators=[RegexValidator(regex='^[a-zA-Zа-яА-Я ]+$', message='Используйте только буквы')],
        required=True,
    )
    status = forms.BooleanField(required=False)

    def clean_email(self):
            description = self.cleaned_data['description']
            if not description:
                raise forms.ValidationError('This field is required')
            return description

    class Meta:
        model = Category
        fields = ('name', 'description', 'status')
        labels = {
            'name': 'Category name',
            'description': 'Category description',
            'status': 'Category status',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ProductForm(forms.ModelForm):
    name = forms.CharField(
        max_length=60, 
        validators=[RegexValidator(regex='^[a-zA-Zа-яА-Я ]+$', message='Используйте только буквы')],
        required=True,
    )
    class Meta:
        model = Product
        fields = ('name', 'description', 'status', 'category_id', 'price')
        labels = {
            'name': 'Product name',
            'description': 'Product description',
            'status': 'Product status',
            'category_id': 'Product category',
            'price': 'Product price',
        }
        category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select category",
        widget=forms.Select(attrs={'class': 'form-control'})
        )      
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category_id': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# class AddToCartForm(forms.Form):
#     quantity = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control', 'value': 1}))
#     product_id = forms.IntegerField(widget=forms.HiddenInput())

#     def add_to_cart(self, user):
#         product_id = self.cleaned_data['product_id']
#         quantity = self.cleaned_data['quantity']

#         try:
#             cart_item = CartItem.objects.get(product_id=product_id)
#             cart_item.quantity += quantity
#             cart_item.save()
#         except CartItem.DoesNotExist:
#             CartItem.objects.create(product_id=product_id, quantity=quantity)

# class UserForm(forms.Form):
#     class Meta:
#         model = get_user_model()
#         fields = (
#             'id',
#             'username',
#         )