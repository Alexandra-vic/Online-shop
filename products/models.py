from django.db import models

from django.core.validators import RegexValidator

from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=60, 
        verbose_name='name',
        unique=True,
        validators=[RegexValidator(regex='^[a-zA-Zа-яА-Я ]+$')]
    )
    description = models.TextField(
        verbose_name='description',
    )
    status = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['-id']


class Product(models.Model):
    name = models.CharField(
        max_length=60, 
        verbose_name='name',
        null=False,
        blank=False,
        unique=True,
    )
    description = models.TextField(
        verbose_name='description',
    )
    status = models.BooleanField(
        default=True,
    )
    category_id = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL,
        null = True,
        related_name='products',
    )
    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=False,
        blank=False,
    )

    def __str__(self):
        return f'{self.name} - {self.description}'
    
    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ['-id']


class Cart(models.Model):
    products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f"Cart {self.pk}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart {self.cart.pk}"

# class CartItem(models.Model):
#     # user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)

