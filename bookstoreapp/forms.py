from django import forms
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from bookstoreapp.models import *

#ordersystem
from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

# Create your forms here.
# class BookForm(forms.ModelForm):

#     class Meta:
#         model = Books
#         fields = ('file', 'image','author',"year_published",'title','price')
    
User = get_user_model()   
#Authentication        
# class CustomerSignUp(UserCreationForm):
#     first_name= forms.CharField(label='First Name' ,error_messages={'required': 'Please enter your first name'})
#     last_name= forms.CharField(label='Last Name',error_messages={'required': 'Please enter your last name'})
#     email= forms.EmailField(label='Email Address' ,help_text='Format: 123@gmail.com, 456@yahoo.com',error_messages={'required': 'Please enter your email address'})

#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields=['first_name','last_name','username','email','password1','password2']

        
#     @transaction.atomic
#     def save(self):
#         user = super().save(commit=False)
#         user.is_customer=True
#         user.save()
#         customer = Customer.objects.create(user=user)
#         customer.first_name = self.cleaned_data.get('first_name')
#         customer.last_name = self.cleaned_data.get('last_name')
#         customer.email = self.cleaned_data.get('email')
#         return user
    
# class AuthorSignUp(UserCreationForm):
#     first_name= forms.CharField(label='First Name' ,error_messages={'required': 'Please enter your first name'})
#     last_name= forms.CharField(label='Last Name',error_messages={'required': 'Please enter your last name'})
#     email= forms.EmailField(label='Email Address' ,help_text='Format: 123@gmail.com, 456@yahoo.com',error_messages={'required': 'Please enter your email address'})

#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields=['first_name','last_name','username','email','password1','password2']

        
#     @transaction.atomic
#     def save(self):
#         user = super().save(commit=False)
#         user.is_author=True
#         user.save()
#         author = Author.objects.create(user=user)
#         author.first_name = self.cleaned_data.get('first_name')
#         author.last_name = self.cleaned_data.get('last_name')
#         author.email = self.cleaned_data.get('email')
#         return user
    
    
    #order system
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('image','name','description', 'price', 'digital','author','year_published')