
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.db import models

#ordersystem
# from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import cloudinary
from cloudinary.models import CloudinaryField

class User(AbstractUser):
    is_author = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_institution = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    email = models.EmailField(max_length=200,null=True,unique=True)
    username = models.CharField(max_length=200,null=True, blank=False)
    REQUIRED_FIELDS = []

    USERNAME_FIELD = 'email'
    
    
class Admin(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)    
    date = models.DateTimeField(auto_now_add=True)

    def save_admin(self):
        self.save()
        
    def update_admin(self):
        self.update()
        
    def delete_admin(self):
        self.delete()
        
    def __str__(self):
      return f'{self.user}'
  
  
class Institution(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def save_institution(self):
        self.save()
        
    def update_institution(self):
        self.update()
        
    def delete_institution(self):
        self.delete()
        
    def __str__(self):
      return f'{self.user}'

#add author table
class Author(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)

    # username = models.CharField(max_length=200,null=True, unique=True)
    # phone_no = models.IntegerField(blank=False, null=True)
    # books_authored = models.CharField(max_length=200, blank=False,default = "e.g anthills of savannah", unique=True)
    # email = models.EmailField(max_length=200,unique=True)
    date = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def save_author(self):
        self.save()
        
    def update_author(self):
        self.update()
        
    def delete_author(self):
        self.delete()
        
    def __str__(self):
      return f'{self.user}'
class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    # fist_name = models.CharField(max_length=200,null=True, blank=False)
    # last_name = models.CharField(max_length=200,null=True, blank=False)
    # username = models.CharField(max_length=200, default="", blank=False)
    # phone_no = models.IntegerField(blank=False,null=True)
    # email = models.EmailField(max_length=200,unique=True,null=True,)
    date = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def save_customer(self):
        self.save()
        
    def update_customer(self):
        self.update()
        
    def delete_customer(self):
        self.delete()
        
    def __str__(self):
      return f'{self.user}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = CloudinaryField("image")
    bio = models.TextField(max_length=250, blank=True, null=True)
    institution_address = models.CharField(max_length=200,null=True, blank=False, unique=True)
    phone_no = models.IntegerField(blank=False, null=True)
    institution_name = models.CharField(max_length=200, null=True,blank=False)
    last_name = models.CharField(max_length=200,null=True, blank=False)
    first_name = models.CharField(max_length=200,null=True, blank=False)

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def filter_by_id(cls, id):
        profile = Profile.objects.filter(user=id).first()
        return profile

    def __str__(self):
        return self.user.username
class Product(models.Model):
    product_name = models.CharField(max_length=200)
    price = models.FloatField()
    digital = models.BooleanField(default=False,null=True, blank=True)
    image = CloudinaryField('image')
    description = models.CharField(max_length=400,default=False)
    author = models.CharField(default='Author name..',max_length=100)
    year_published = models.IntegerField(blank=True, null=True)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    
    
        # get images by user
    @classmethod
    def get_images_by_user(cls, user):
        products = cls.objects.filter(user=user)
        return products

    @property
    def save_image(self):
          self.save()
          
    def update_image(self):
        self.update()

    def delete_image(self):
        self.delete()
        
    def __str__(self):
      return f'{self.product_name}'

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
    
    
# likes model
class Likes(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # likes = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.product
    
class Comments(models.Model):
  comment = models.TextField()
  product = models.ForeignKey(Product,default="", on_delete=models.CASCADE)
  date = models.DateTimeField(auto_now_add=True)
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  

  
  def save_user_comment(self):
        self.save()
  def update_user_comment(self):
        self.update()
  def delete_user_comment(self):
        self.delete()
  
  def __str__(self):
    return f'{self.user}'