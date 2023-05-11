
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.db import models

#ordersystem
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import cloudinary
from cloudinary.models import CloudinaryField

# Create your models here.
# class Books(models.Model):
   # file = models.FileField(upload_to='documents/')
   # image = models.ImageField(upload_to='images/')
   # author = models.CharField(default='Author name..',max_length=100)
   # year_published = models.IntegerField(blank=True, null=True)
   # title = models.CharField(default='Title of the book',max_length=100)
   # price = models.IntegerField(blank=True, null=True,default='Price in dollars..')
   
   
   
#Author

#create custoclass User(AbstractUser):
# class User(AbstractUser):
#     is_customer = models.BooleanField(default=False)
#     is_author = models.BooleanField(default=False)

# class Customer(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


# class Author(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    
    #ordersystem
class Profile(models.Model):
  profile_photo= CloudinaryField('image')
  bio = models.TextField()
  username = models.CharField(max_length=200, unique=True)
  email = models.EmailField(max_length=30)
  phone_no = models.IntegerField(blank=False)
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  date = models.DateTimeField(auto_now_add=True)
  modified = models.DateTimeField(auto_now=True)
  
  def save_user(self):
        self.save()
  def update_user(self):
        self.update()
  def delete_user(self):
        self.delete()
  
  def __str__(self):
    return f'{self.user}'

#add author table
class Author(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    username = models.CharField(max_length=200, null=True)
    fname = models.CharField(max_length=200, null=True)
    lname = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)
    book_authored = models.CharField(max_length=200, blank=False, unique=True)

    def save_author(self):
        self.save()
    def update_author(self):
        self.update()
    def delete_author(self):
        self.delete()
        
    def __str__(self):
      return f'{self.user}'
class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    username = models.CharField(max_length=200, null=True)
    fname = models.CharField(max_length=200, null=True)
    lname = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)


    def save_customer(self):
        self.save()
    def update_customer(self):
        self.update()
    def delete_customer(self):
        self.delete()
        
    def __str__(self):
      return f'{self.user}'

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    digital = models.BooleanField(default=False,null=True, blank=True)
    image = CloudinaryField('image')
    description = models.CharField(max_length=400,default=False)
    author = models.CharField(default='Author name..',max_length=100)
    year_published = models.IntegerField(blank=True, null=True)
   
   
    def __str__(self):
      return self.name

    @property
    def save_image(self):
          self.save()
          
    def update_image(self):
        self.update()

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

@receiver(post_save, sender=User)
def create_user_customer(sender, instance, created, **kwargs):
  if created:
    print('created')
    Customer.objects.create(user=instance)