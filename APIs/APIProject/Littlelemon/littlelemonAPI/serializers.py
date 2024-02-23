from rest_framework import serializers
from .models import Category, Menuitem, Cart, Order, OrderItem
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta():
        model = Menuitem
        fields = ['id','title', 'price', 'featured', 'category']
        depth = 1
        
class CategorySerializer(serializers.Serializer):
    class Meta:
        model = Category
        fields = ['slug']
        
class ManagerSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        
class CartHelpSerializer(serializers.Serializer):
    class Meta:
        model = Menuitem
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
        model = Menuitem
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