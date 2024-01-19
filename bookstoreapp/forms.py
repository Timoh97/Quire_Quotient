from django import forms
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from bookstoreapp.models import *
from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.utils.text import capfirst


from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer,Product
from .models import Customer, Author


# Create your forms here.

class UserRegistrationForm(UserCreationForm):
    USER_TYPES = [
        ('Author', 'Author'),
        ('Customer', 'Customer'),
    ]
    user_type = forms.ChoiceField(choices=USER_TYPES, required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    zen_name = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'zen_name', 'user_type']

    def save(self, commit=True):
        user = super().save(commit=False)
        # Set username to None
        user.username = self.cleaned_data['email']
        user.is_author = (self.cleaned_data['user_type'] == 'Author')
        user.is_customer = (self.cleaned_data['user_type'] == 'Customer')

        if commit:
            user.save()
        return user
        

class CustomerForm(UserRegistrationForm):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    bio = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    profile_photo = forms.ImageField()
   
    class Meta:
        model = Customer
        fields = [ 'phone_number', 'bio','address','first_name', 'last_name','profile_photo']


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off'}))
class AuthorForm(UserRegistrationForm):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    bio = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    profile_photo = forms.ImageField()
    
    class Meta:
        model = Author
        fields = [  'phone_number', 'bio','address','first_name', 'last_name','profile_photo']
class OTPVerificationForm(forms.Form):
    otp = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('image','name', 'price', 'digital')
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name','last_name','profession','phone_number','address','facebook_url','twitter_url','instagram_url','linkedin_url','bio']  
        
    def __init__(self, *args, **kwargs):
        super(CustomerProfileForm, self).__init__(*args, **kwargs)

        # Set the first six fields as required
        required_fields = ['first_name', 'last_name', 'profession', 'address', 'phone_number','bio']
        for field_name in required_fields:
            self.fields[field_name].required = True
            self.fields[field_name].widget.attrs['autocomplete'] = 'off'

        # Disable autocomplete for the entire form
        # self.fields['first_name'].widget.attrs['autocomplete'] = 'off'
        # self.fields['last_name'].widget.attrs['autocomplete'] = 'off'
        # self.fields['profile_photo'].widget.attrs['autocomplete'] = 'off'
        # self.fields['profession'].widget.attrs['autocomplete'] = 'off'
        # self.fields['level'].widget.attrs['autocomplete'] = 'off'
        # self.fields['phone_number'].widget.attrs['autocomplete'] = 'off'
        # self.fields['bio'].widget.attrs['autocomplete'] = 'off'
        # Add similar lines for other fields if needed    
class AuthorProfileForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = [ 'first_name','last_name','designation','level','phone_number','address','facebook_url','twitter_url','instagram_url','dribble_url','linkedin_url','bio'] 
        
        
    def __init__(self, *args, **kwargs):
        super(AuthorProfileForm, self).__init__(*args, **kwargs)

        # Set the first six fields as required
        required_fields = ['first_name', 'last_name',  'designation', 'level', 'phone_number','bio']
        for field_name in required_fields:
            self.fields[field_name].required = True
            self.fields[field_name].widget.attrs['autocomplete'] = 'off'

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']

# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ('image','product_name','description', 'price', 'digital','author','year_published')