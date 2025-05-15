from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    phone_number=models.CharField(max_length=200)
    address=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    user_img=models.ImageField(upload_to='uploads/')

    def __str__(self):
        return self.name
class Seller(models.Model):
    seller=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(  max_length=200)
    phone_number=models.CharField(max_length=200)
    business_type=models.CharField(max_length=200,choices=[
        ('Individual', 'Individual'),
        ('Retailer', 'Retailer'),
        ('Wholesaler', 'Wholesaler'),

    ] ,default='Individual')
    profile_image = models.ImageField(upload_to='seller_profiles/', blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
class Product(models.Model):
    p_name=models.CharField(max_length=200)
    description=models.TextField()
    categories =models.CharField(max_length=200)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.PositiveIntegerField()
    image_url =models.ImageField(upload_to='uploads/')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.p_name} - {self.seller.name}"

class Worker(models.Model):
    PRICE_TYPE_CHOICES = [
        ('day', 'Per Day'),
        ('hour', 'Per Hour'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    work_category = models.CharField(max_length=100)
    work_name = models.CharField(max_length=100)
    price_type = models.CharField(max_length=10, choices=PRICE_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=255, null=True, blank=True)
    experience = models.TextField(null=True, blank=True)
    availability = models.BooleanField(default=True)
    image = models.ImageField(upload_to='worker_images/', null=True, blank=True)
    ragting = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)


    def __str__(self):
        return self.name
class Worker_image(models.Model):
    Worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='work_images')
    images = models.ImageField(upload_to='uploads/')
      
  
    def __str__(self):
        return f"Image for {self.Worker.name}"
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address_line = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.address_line}, {self.city}, {self.state}, {self.country}"
class Hire(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='hires')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hires')
    hire_date = models.DateTimeField(default=timezone.now)
    worker_count = models.PositiveIntegerField(default=1)
    address=models.ForeignKey(Address, on_delete=models.CASCADE, related_name='hires')
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ], default='pending')
    phone_number = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"Hire {self.id} - {self.worker.name}"
class Product_Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image for {self.product.p_name}"
class Order(models.Model):
    Seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='orders')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    expected_delivery_date = models.DateTimeField(null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='orders')
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  
    
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ], default='pending')

    def __str__(self):
        return f"Order {self.id} - {self.product.p_name}"
class Kart(models.Model):
 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='karts')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='karts')
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} - {self.product.p_name}"
    















   
   