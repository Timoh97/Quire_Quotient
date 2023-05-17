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
class AuthorSignUpForm(UserCreationForm):
    username= forms.CharField(error_messages={'required': 'Please enter the username'})
    email= forms.EmailField(help_text='Format: 123@gmail.com, 456@yahoo.com',error_messages={'required': 'Please enter your email address'})

    class Meta(UserCreationForm.Meta):
        model = User
        fields=["username",'email','password1','password2']
        
        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_author=True
        user.save()
        return user
    


#Customer registration form    
class CustomerSignUpForm(UserCreationForm):
    username= forms.CharField(error_messages={'required': 'Please enter the username'})
    email= forms.EmailField(help_text='Format: 123@gmail.com, 456@yahoo.com',error_messages={'required': 'Please enter your email address'})

    class Meta(UserCreationForm.Meta):
        model = User
        fields=["username",'email','password1','password2']

        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer=True
        user.save()
        return user

    #institution registration form
class InstitutionSignUpForm(UserCreationForm):
    username= forms.CharField(help_text='Enter the name of the institution',error_messages={'required': 'Please enter the institution name'})
    email= forms.EmailField(help_text='Format: 123@kenyatta.university.com, 456@student.uon.com',error_messages={'required': 'Please enter your email address'})
    class Meta(UserCreationForm.Meta):
        model = User
        fields=["username",'email','password1','password2']

        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_institution=True
        user.save()
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
    
#updating various profiles

# class UpdateProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ["profile_photo","bio","phone_no","first_name","last_name","address","username"]
# class UpdateCustomerProfileForm(forms.ModelForm):
#     class Meta:
#         model = Customer
#         exclude = ['user','modified','date']
        
# class UpdateAuthorProfileForm(forms.ModelForm):
#     class Meta:
#         model = Author
#         exclude = ['user','modified','date']
# class UpdateCommentForm(forms.ModelForm):
#     class Meta:
#         model = Comments
#         exclude = ['user']
         
# class UpdateInstitutionProfileForm(forms.ModelForm):
#     class Meta:
#         model = Institution
#         exclude = ['user','modified','date']



# class UpdateUserProfile(forms.ModelForm):
#   class Meta:
#     model = Customer
#     exclude = ['user']



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('image','product_name','description', 'price', 'digital','author','year_published')