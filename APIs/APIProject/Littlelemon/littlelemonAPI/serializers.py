from rest_framework import serializers
from .models import Menuitem
from decimal import Decimal

class MenuItemSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source = 'inventory')
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    
    class Meta:
        model = Menuitem
        fields = ['id', 'title', 'stock','price']
        
    def calculateTax(self, product:Menuitem):
        return product.price * Decimal(1.1) 