from django.shortcuts import render
# Create your views here.
from rest_framework import generics
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
# views.py
from rest_framework import generics
from .models import CustomUser
from .serializers import CustomUserSerializer

class CustomUserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class CustomUserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
# views.py

from rest_framework import generics
from .models import CartItem
from .serializers import CartItemSerializer

class CartItemList(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(user=user)

class CartItemDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(user=user)
    


# views.py

from rest_framework import generics
from rest_framework.response import Response
from .models import Checkout
from .serializers import CheckoutSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny  

class CheckoutCreateView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer

    def perform_create(self, serializer):
        # Associate the checkout with the current user
        serializer.save(user=self.request.user)

class CheckoutDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer

# views.py

# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import stripe
from django.conf import settings
from .models import Order
from .serializers import OrderSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
@permission_classes([AllowAny])
class PaymentView(APIView):
    def post(self, request, *args, **kwargs):
        order_id = request.data.get('order_id')

        try:
            order = Order.objects.get(order_id=order_id)
        except Order.DoesNotExist:
            return Response({'error': f'Order with order_id {order_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)

        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Use the serializer to validate the payment information
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            token = request.data.get('token')

            try:
                charge = stripe.Charge.create(
                    amount=int(order.total_amount * 100),
                    currency="usd",
                    source=token,
                    description=f"Charge for {order}",
                )

                order.paid = True
                order.save()

                return Response({'message': 'Payment successful'}, status=status.HTTP_200_OK)

            except stripe.error.CardError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
