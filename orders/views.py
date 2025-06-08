from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from cart.models import Cart
from .models import Order, OrderItem
from .serializers import OrderSerializer, CreateOrderSerializer

# Create your views here.

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    

class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    

@api_view(['POST'])
def create_order(request):
    serializer = CreateOrderSerializer(data=request.data)
    if serializer.is_valid():
        try:
            cart = Cart.objects.get(user=request.user)
            if not cart.items.exists(): # type: ignore
                return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check stock availability
            for item in cart.items.all():
                if item.product.stock < item.quantity:
                    return Response({
                        'error' : f'Insufficient stock for {item.product.name}'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                #Create Order
            order = Order.objects.create(
                user = request.user,
                total_amount = cart.total_price,
                shipping_address = serializer.validated_data['shipping_address']
            )

                # Create order items and update stock
            for item in cart.items.all():
                OrderItem.objects.create(
                    order = order,
                    product = item.product,
                    quantity = item.quantity,
                    price = item.product.price
                )
                item.product.stock -= item.quantity
                item.product.save()

                # Clear cart
                cart.items.all().delete()

                return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
            
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        