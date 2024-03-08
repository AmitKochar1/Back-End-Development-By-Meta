from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta():
        model = MenuItem
        fields = ['id','title', 'price', 'featured', 'category']
        depth = 1
        
class CategorySerializer(serializers.Serializer):
    class Meta:
        model = Category
        fields = ['slug']
        
class ManagerListMenuItemSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        
class CartHelpSerializer(serializers.Serializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'user']
        
class CartSerializer(serializers.Serializer):
    menuitem = CartHelpSerializer()
    class Meta:
        model = Cart
        fields = ['menuitem', 'quantity', 'price']

class CartAddSerializer(serializers.Serializer):
    class Meta:
        model = Cart
        fields = ['menuitem', 'quantity']
        extra_kwargs = {
            'quantity': {'min_value':1},
        }
        
class CartRemoveSerializer(serializers.Serializer):
    class Meta:
        model = Cart
        fields = ['menuitem']
        
class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields=['username']
        
class OrderSerializer(serializers.Serializer):
    user = UserSerializer()
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date']
        
class SingleHelperSerializer(serializers.Serializer):
    class Meta:
        model = MenuItem
        fields = ['title', 'price']
        
class SingleOrderSerializer(serializers.Serializer):
    menuitem = SingleHelperSerializer()
    class Meta:
        model = OrderItem
        fields = ['menuitem', 'quantity']
        
class OrderPutSerializer(serializers.Serializer):
    class Meta:
        model = Order
        fields = ['delivery_crew']
        
        
        
# As per Meta 
# from rest_framework import serializers
# from django.contrib.auth.models import User
# from decimal import Decimal

# from .models import Category, MenuItem, Cart, Order, OrderItem


# class CategorySerializer (serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['id', 'title', 'slug']


# class MenuItemSerializer(serializers.ModelSerializer):
#     category = serializers.PrimaryKeyRelatedField(
#         queryset=Category.objects.all()
#     )
#     # category = CategorySerializer(read_only=True)
#     class Meta:
#         model = MenuItem
#         fields = ['id', 'title', 'price', 'category', 'featured']


# class CartSerializer(serializers.ModelSerializer):
#     user = serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.all(),
#         default=serializers.CurrentUserDefault()
#     )


#     def validate(self, attrs):
#         attrs['price'] = attrs['quantity'] * attrs['unit_price']
#         return attrs

#     class Meta:
#         model = Cart
#         fields = ['user', 'menuitem', 'unit_price', 'quantity', 'price']
#         extra_kwargs = {
#             'price': {'read_only': True}
#         }


# class OrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = ['order', 'menuitem', 'quantity', 'price']


# class OrderSerializer(serializers.ModelSerializer):

#     orderitem = OrderItemSerializer(many=True, read_only=True, source='order')

#     class Meta:
#         model = Order
#         fields = ['id', 'user', 'delivery_crew',
#                   'status', 'date', 'total', 'orderitem']


# class UserSerilializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id','username','email']