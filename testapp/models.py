from django.db import models

# Create your models here.
#from testapp.models import CustomUser
from django.contrib.auth.models import AbstractUser
#from django.db import models

class CustomUser(AbstractUser):
    # Add your custom fields here
    email = models.EmailField(unique=True)
    username=models.CharField(max_length=60)
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    
    USERNAME_FIELD = 'email'  # Use 'email' as the unique identifier for authentication
    REQUIRED_FIELDS = ['username'] 

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=255)

class Product(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

# models.py
from django.db import models
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Assuming you have a User model

# models.py

from django.db import models
from testapp.models import CustomUser  

class Checkout(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    shipping_address = models.TextField()
    payment_method = models.CharField(max_length=50)
    
# models.py

from django.db import models

class Order(models.Model):
    # Your order fields here
    order_id = models.CharField(max_length=10, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Payment information
    card_number = models.CharField(max_length=16)
    expiry_date = models.CharField(max_length=5)  # Assuming MM/YY format
    cvv = models.CharField(max_length=3)

    # ...

    def __str__(self):
        return f"Order #{self.id}"
