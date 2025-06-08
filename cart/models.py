from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

# Create your models here.
User = get_user_model()

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart - {self.user.username}"
    
    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all()) # type: ignore
    
    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all()) # type: ignore
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['cart', 'product']

    def __str__(self):
        return f"{self.product.name} * {self.quantity}"

    @property
    def total_price(self):
        return self.product.price * self.quantity    