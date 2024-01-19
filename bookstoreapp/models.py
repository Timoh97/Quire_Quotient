from django.db import models
from django.contrib.auth.models import BaseUserManager

from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
import cloudinary
from cloudinary.models import CloudinaryField
from django.urls import reverse

# Create your models here.
# Custom user manager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_author(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_author', True)
        user = self.create_user(email, password, **extra_fields)
        Author.objects.create(user=user)
        return user

    def create_customer(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_customer', True)
        user = self.create_user(email, password, **extra_fields)
        Customer.objects.create(user=user)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

    
class User(AbstractUser):
    email = models.EmailField(unique=True)
    zen_name = models.CharField(max_length=200, null=True)
    is_active = models.BooleanField(default=True)
    is_author = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    # username = models.CharField(max_length=200, unique=True)  # Add this line

    objects = UserManager()
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    
    class Meta:
        app_label = 'bookstoreapp'

    def __str__(self):
        return self.email
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_customer:
            Customer.objects.create(user=instance)
        elif instance.is_author:
            Author.objects.create(user=instance)
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.IntegerField(blank=True, null=True)
    bio = models.TextField(max_length=250, blank=True, null=True)
    address = models.CharField(max_length=200,null=True, blank=False, unique=True)
    first_name = models.CharField(max_length=200,null=True, blank=False)
    last_name = models.CharField(max_length=200,null=True, blank=False)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expires_at = models.DateTimeField(null=True, blank=True)
    profile_photo = CloudinaryField("image")
    profession = models.CharField(max_length=15, null=True, blank=True)
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    user_type = models.CharField(max_length=10, choices=[('Customer', 'Customer')])

    
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.IntegerField(blank=True, null=True)
    bio = models.TextField(max_length=250, blank=True, null=True)
    address = models.CharField(max_length=200,null=True, blank=False, unique=True)
    first_name = models.CharField(max_length=200,null=True, blank=False)
    last_name = models.CharField(max_length=200,null=True, blank=False)
    profile_photo = CloudinaryField("image")
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expires_at = models.DateTimeField(null=True, blank=True)
    designation = models.CharField(max_length=15, null=True, blank=True)
    level = models.CharField(max_length=15, null=True, blank=True)
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    dribble_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    user_type = models.CharField(max_length=10, choices=[('Author', 'Author')])

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    digital = models.BooleanField(default=False,null=True, blank=True)
    image = CloudinaryField('image')

    def __str__(self):
      return self.name

    @property
    def save_image(self):
          self.save()

    def delete_image(self):
        self.delete()

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)
		
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Product, on_delete=models.CASCADE)  # Replace 'Book' with your actual book model
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('book_detail', args=[str(self.book.id)])
    
    
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Replace Product with your actual product model
    rating = models.IntegerField(default=0, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    created_at = models.DateTimeField(auto_now_add=True)