
from django.urls import path
from .views import *

urlpatterns = [
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('products/', ProductList.as_view(), name='product-list'),
    path('cart/', CartItemList.as_view(), name='cart-list'),
    path('cart/<int:pk>/', CartItemDetail.as_view(), name='cart-detail'),
    path('users/', CustomUserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', CustomUserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),
    path('checkout/', CheckoutCreateView.as_view(), name='checkout-create'),
    path('checkout/<int:pk>/', CheckoutDetailView.as_view(), name='checkout-detail'),
    path('payment/', PaymentView.as_view(), name='payment'),
    
]
