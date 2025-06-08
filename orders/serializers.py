from rest_framework import serializers
from products.serializers import ProductListSerializer
from . models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['user', 'total_amount']


class CreateOrderSerializer(serializers.Serializer):
    shipping_address = serializers.CharField(max_length=500)