from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from products.models import Product
from .models import Cart, CartItem
from .serializers import CartSerializer, AddToCartSerializer

# Create your views here.

class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    
    def get_object(self): # type: ignore
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart


@api_view(['POST'])
def add_to_cart(request):
    serializer = AddToCartSerializer(data=request.data)
    if serializer.is_valid():
        product_id = serializer.validated_data['product_id'] # type: ignore
        quantity = serializer.validated_data['quantity'] # type: ignore
        
        try:
            product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if product.stock < quantity:
            return Response({'error': 'Insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)
        
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, 
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            if cart_item.quantity > product.stock:
                return Response({'error': 'Insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)
            cart_item.save()
        
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def remove_from_cart(request, item_id):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(id=item_id, cart=cart)
        cart_item.delete()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['PATCH'])
def update_cart_item(request, item_id):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(id=item_id, cart=cart)
        
        quantity = request.data.get('quantity')
        if quantity and quantity > 0:
            if quantity > cart_item.product.stock:
                return Response({'error': 'Insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)
            cart_item.quantity = quantity
            cart_item.save()
            return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid quantity'}, status=status.HTTP_400_BAD_REQUEST)
    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)