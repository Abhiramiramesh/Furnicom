# from django.db import models
# from django.contrib.auth.models import AbstractUser, BaseUserManager

# # Create your models here.
# class User(AbstractUser):
#     phone = models.CharField(max_length=15)
#     profile = models.ImageField(upload_to="profile/")





from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# from django.contrib import admin
# from .models import Customisedorder
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


# Custom user model
class User(AbstractUser):
    email = models.EmailField(unique=True)  
    phone = models.CharField(max_length=15, null=True, blank=True)
    fullname = models.CharField(max_length=100, null=True, blank=True)
    
    profile = models.ImageField(upload_to="profile/")
    role = models.CharField(max_length=100, null=True, blank=True)
    username = None

    objects = CustomUserManager()

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.fullname
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Product(models.Model):
    productname = models.CharField(max_length=100, null=True, blank=True)  
    productprice = models.DecimalField(max_digits=10, decimal_places=2)
    profile = models.ImageField(upload_to="profile/")
    

    


class Colour(models.Model):
    colourname = models.CharField(max_length=100, null=True, blank=True) 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="profile/")

    def __str__(self):
        return self.colourname

class Wood(models.Model):
    woodtype = models.CharField(max_length=100, null=True, blank=True) 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="profile/")

    def __str__(self):
        return self.woodtype

class Category(models.Model):
    category = models.CharField(max_length=100, null=True, blank=True) 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="profile/")

    def __str__(self):
        return self.category


    
# class Carpenter(models.Model):
#     carpenter = models.CharField(max_length=100, null=True, blank=True)
#     email = models.EmailField(unique=True)  
#     phone = models.CharField(max_length=15, null=True, blank=True)
#     password = models.ch

class Customisedorder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    colour = models.ForeignKey('Colour', on_delete=models.SET_NULL, null=True)
    wood = models.ForeignKey('Wood', on_delete=models.SET_NULL, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s order"
    


class Productorder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    ordered_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s order"
    

    


    # CartItem model — stores which product a user has added to their cart
class Cartitem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Each cart is tied to a user
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # How many of this product

    # Method to calculate total price for this item
    def total_price(self):
        return self.product.productprice * self.quantity

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
    

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cardholder_name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=16)
    expiry_date = models.CharField(max_length=5)  # Format: MM/YY
    cvv = models.CharField(max_length=3)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment by {self.user.username} of ₹{self.amount}"

    
# @admin.register(Customisedorder)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('user', 'category', 'color', 'wood', 'total_price', 'ordered_at')
    

