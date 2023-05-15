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
    first_name= forms.CharField(error_messages={'required': 'Please enter your first name'})
    last_name= forms.CharField(error_messages={'required': 'Please enter your last name'})
    username= forms.CharField(error_messages={'required': 'Please enter the username'})
    phone_no= forms.IntegerField(error_messages={'required': 'Please enter your phone number'})
    email= forms.EmailField(help_text='Format: 123@gmail.com, 456@yahoo.com',error_messages={'required': 'Please enter your email address'})

    class Meta(UserCreationForm.Meta):
        model = User
        fields=['first_name','last_name',"username",'phone_no','email','password1','password2']
        
        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_author=True
        user.save()
        author = Author.objects.create(user=user)
        author.first_name = self.cleaned_data.get('first_name')
        author.last_name = self.cleaned_data.get('last_name')
        author.username = self.cleaned_data.get("username", None)
        author.phone_no = self.cleaned_data.get('phone_no')
        author.email = self.cleaned_data.get('email')
        return user
    


#Customer registration form    
class CustomerSignUpForm(UserCreationForm):
    first_name= forms.CharField(error_messages={'required': 'Please enter your first name'})
    last_name= forms.CharField(error_messages={'required': 'Please enter your last name'})
    username= forms.CharField(error_messages={'required': 'Please enter the username'})
    phone_no= forms.IntegerField(error_messages={'required': 'Please enter your phone number'})
    email= forms.EmailField(help_text='Format: 123@gmail.com, 456@yahoo.com',error_messages={'required': 'Please enter your email address'})

    class Meta(UserCreationForm.Meta):
        model = User
        fields=['first_name','last_name',"username",'phone_no','email','password1','password2']

        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer=True
        user.save()
        customer =Customer.objects.create(user=user)
        customer.first_name = self.cleaned_data.get('first_name')
        customer.last_name = self.cleaned_data.get('last_name')
        customer.username = self.cleaned_data.get("username", None)
        customer.phone_no = self.cleaned_data.get('phone_no')
        customer.email = self.cleaned_data.get('email')
        return user
    
    #institution registration form
class InstitutionSignUpForm(UserCreationForm):
    institution_name= forms.CharField(error_messages={'required': 'Please enter the institution name'})
    username= forms.CharField(error_messages={'required': 'Please enter the username'})
    phone_no= forms.IntegerField(error_messages={'required': 'Please enter the institution phone number'})
    institution_address= forms.CharField(error_messages={'required': 'Please enter the institution address'})
    email= forms.EmailField(help_text='Format: 123@gmail.com, 456@yahoo.com',error_messages={'required': 'Please enter your email address'})

    class Meta(UserCreationForm.Meta):
        model = User
        fields=['institution_name',"username",'phone_no','institution_address','email','password1','password2']

        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_institution=True
        user.save()
        institution =Institution.objects.create(user=user)
        institution.institution_name = self.cleaned_data.get('institution_name')
        institution.username = self.cleaned_data.get("username", None)
        institution.phone_no = self.cleaned_data.get('phone_no')
        institution.institution_address = self.cleaned_data.get('institution_address')
        institution.email = self.cleaned_data.get('email')
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


class UpdateCustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ['user','modified','date']
        
class UpdateAuthorProfileForm(forms.ModelForm):
    class Meta:
        model = Author
        exclude = ['user','modified','date']
class UpdateCommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        exclude = ['user']
         
class UpdateInstitutionProfileForm(forms.ModelForm):
    class Meta:
        model = Institution
        exclude = ['user','modified','date']



# class UpdateUserProfile(forms.ModelForm):
#   class Meta:
#     model = Customer
#     exclude = ['user']



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('image','product_name','description', 'price', 'digital','author','year_published')