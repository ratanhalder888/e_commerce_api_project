from django.urls import path
from . import views


urlpatterns = [
    path('',views.ProductListView.as_view(), name='product-list'),
    path('categories/', views.CategoryListView.as_view(), name='categories-list'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('<int:product_id>/reviews/', views.ProductReviewListView.as_view(), name='product-reviews'),
    path('<int:product_id>/reviews/create/', views.ProductReviewCreateView.as_view(), name='create-review')
]
