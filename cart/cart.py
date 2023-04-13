from decimal import Decimal
from django.conf import settings
from django.contrib.auth.models import User
from products.models import Product, Cart, CartItem



class Cart(object):

    def __init__(self, request):
        # Инициализация корзины пользователя
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Сохраняем корзину пользователя в сессию
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

        # Итерация по товарам
    def __iter__(self):
        products_ids = self.cart.keys()
        products = Product.objects.filter(id__in=products_ids)

        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item     

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values()) 
        

    # Добавление товар в корзину пользователя
    # или обновление количества товаров
    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()


        # if self.cart:
        #     for item in self.cart:
        #         if item['product_id'] == str(product.id):
        #             if update_quantity:
        #                 if (product_id.amount - quantity) < 0:
        #                     return False
        #                 else:
        #                     item['quantity'] = quantity 
        #             else:
        #                 if (product_id.amount - item['quantity'] - quantity) < 0:
        #                     return False
        #                 else:
        #                     item['quantity'] += 1
        #             self.save()
        #             return True  
        #     for item in self.cart:
        #         if item['product_id'] != str(product.id):
        #             self.cart.append(new_product)
        #             self.save()
        #             return True    
        # else:
        #     self.cart.append(new_product)
        #     self.save()
        #     return True
        
        # if product_id not in self.cart:
        #     self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        # if update_quantity:
        #     self.cart[product_id]['quantity'] = quantity
        # else:
        #     self.cart[product_id]['quantity'] += quantity
        # self.save()

     # Сохранение данных в сессию
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True     

    # Удаление товара из корзины
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()      

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())


    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True    
