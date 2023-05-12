from django import forms
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from bookstoreapp.models import *
from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.utils.text import capfirst

#author registration form
class AuthorSignUp(UserCreationForm):
    fname= forms.CharField(error_messages={'required': 'Please enter your first name'})
    lname= forms.CharField(error_messages={'required': 'Please enter your last name'})
    username= forms.CharField(error_messages={'required': 'Please enter your username'})
    phone_no= forms.IntegerField(error_messages={'required': 'Please enter your phone number'})
    books_authored= forms.CharField(error_messages={'required': 'Please enter your last name'})
    email= forms.EmailField(help_text='Format: 123@gmail.com, 456@yahoo.com',error_messages={'required': 'Please enter your email address'})

    class Meta(UserCreationForm.Meta):
        model = User
        fields=['fname','lname','username','phone_no','books_authored','email','password1','password2']
        
        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_author=True
        user.save()
        author = Author.objects.create(user=user)
        author.fname = self.cleaned_data.get('fname')
        author.lname = self.cleaned_data.get('lname')
        author.username = self.cleaned_data.get('username')
        author.phone_no = self.cleaned_data.get('phone_no')
        author.books_authored = self.cleaned_data.get('books_authored')
        author.email = self.cleaned_data.get('email')
        return user
    


#Customer registration form    
class CustomerSignUp(UserCreationForm):
    fname= forms.CharField(error_messages={'required': 'Please enter your first name'})
    lname= forms.CharField(error_messages={'required': 'Please enter your last name'})
    username= forms.CharField(error_messages={'required': 'Please enter your username'})
    phone_no= forms.IntegerField(error_messages={'required': 'Please enter your phone number'})
    email= forms.EmailField(help_text='Format: 123@gmail.com, 456@yahoo.com',error_messages={'required': 'Please enter your email address'})

    class Meta(UserCreationForm.Meta):
        model = User
        fields=['fname','lname','username','phone_no','email','password1','password2']

        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer=True
        user.save()
        customer =Customer.objects.create(user=user)
        customer.fname = self.cleaned_data.get('fname')
        customer.lname = self.cleaned_data.get('lname')
        customer.username = self.cleaned_data.get('username')
        customer.phone_no = self.cleaned_data.get('phone_no')
        customer.email = self.cleaned_data.get('email')
        return user

#author and customer have same login form
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class":"form-control"
            }
        )
    )

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('image','product_name','description', 'price', 'digital','author','year_published')