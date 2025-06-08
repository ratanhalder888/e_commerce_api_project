from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrderListView.as_view(), name='order-list'),
    path('create/', views.create_order, name='create-order'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
]