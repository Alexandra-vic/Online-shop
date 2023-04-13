from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from products import views


home_page = [
    # path('', views.get_home_page, name='home'),
    path('categories/new/', views.CategoryCreateView.as_view(), name='create'),
    path('categories/', views.CategoryView.as_view(), name='category'),
    path('category-update/<int:pk>/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('category-delete/<int:pk>/', views.CategoryDeleteView.as_view(), name='category_delete'),
    # path('cart/products/', views.ProductView.as_view(), name='cart/products'),
    path('products/', views.ProductAllView.as_view(), name='product'),

    path('', views.ProductListView.as_view(), name='home'),
    path('product/new/', views.ProductCreateView.as_view(), name='product_create'),
    path('product-delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('product-update/<int:pk>/', views.ProductUpdateView.as_view(), name='product_update'),

    path('cart/add/', views.cart, name='cart'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(home_page)),
    path('cart/', include('cart.urls', namespace='cart')),
]
