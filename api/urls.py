from django.urls import path
from .views import CategoryListView, ProductListView, OrderCreateView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('orders/', OrderCreateView.as_view(), name='order-create'),
]