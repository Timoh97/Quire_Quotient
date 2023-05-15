from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import *
from .models import *

#AUTHENTICATION
from django.shortcuts import render,redirect
from django.contrib.auth import login, logout,authenticate
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from .forms import *
from. decorators import *
from django.contrib.auth.decorators import *
from django.contrib.auth.decorators import login_required

#ordersystem
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404,HttpResponseRedirect, JsonResponse
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
import json
import datetime
from .models import *
from .forms import *
from .utils import cookieCart, cartData, guestOrder



def signup(request):
    '''View function to present users with account choices'''
    title = 'Sign Up'
    return render(request,'registration/signup.html',{'title': title})

#customer signup
def customer_signup(request):
    '''View function to sign up as a customer'''
    
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            email = form.cleaned_data['email']
            # user = authenticate(username=username, email= email, password=raw_password)
            login(request, user,backend='django.contrib.auth.backends.ModelBackend')
            
            # subject = 'Welcome to the Zen Bookstore!'
            # message = f'Hi {user.username},\nWe officially welcome you to our growing community.\nRemember to enjoy the app!\n\nKind Regards,\nThe Zen-Bookstore App Management.'
            # email_from = settings.EMAIL_HOST_USER
            # recepient_list = [user.email]
            # send_mail(subject,message,email_from,recepient_list)
            messages.success(request, 'Account created successfully! Check your email for a welcome mail.')

            return redirect('/login')
    else:
        form= CustomerSignUpForm()

    # title = 'Welcome, we hold you in high esteem'
    return render(request,'registration/signup_form.html',{'form':form}) #change template


def author_signup(request):
    if request.method == 'POST':
        form = AuthorSignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data['email']
            # user = authenticate(username=username,email=email, password=raw_password)
            login(request, user,backend='django.contrib.auth.backends.ModelBackend')
            # subject = 'Welcome to the Zen Bookstore!'
            # message = f'Hi {user.username},\nWe officially welcome you to our growing community.\nFeel free to sell your books with us!\n\nKind Regards,\nThe Zen-Bookstore App Management.'
            # email_from = settings.EMAIL_HOST_USER
            # recepient_list = [user.email]
            # send_mail(subject,message,email_from,recepient_list)
            messages.success(request, f'Your account has been created! You are now able to log in as {username}.')
            return redirect('login')
    else:
        form = AuthorSignUpForm()
        
    return render(request, 'registration/register.html', {'form':form}) #check template


def institution_signup(request):
    if request.method == 'POST':
        form = InstitutionSignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data['email']
            raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=username,email=email, password=raw_password)
            login(request, user,backend='django.contrib.auth.backends.ModelBackend')
            # subject = 'Welcome to the Zen Bookstore!'
            # message = f'Hi {user.username},\nWe value institutions like yours and welcome you to our growing community.\nYou can purchase books in our app!\n\nKind Regards,\nThe Zen-Bookstore App Management.'
            # email_from = settings.EMAIL_HOST_USER
            # recepient_list = [user.email]
            # send_mail(subject,message,email_from,recepient_list)
            messages.success(request, f'Your account has been created! You are now able to log in {username}.')
            return redirect('login')
    else:
        form = InstitutionSignUpForm()
        title = 'Welcome, we hold you in high esteem'
    return render(request, 'registration/register.html', {'title': title,'form':form}) #check template


def login_view(request):
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("/")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = LoginForm()
	return render(request=request, template_name="login.html", context= {"form":form}) #changetemplate

def logout_view(request):
    logout(request)
    return redirect('/')


#profiles

@customer_required(login_url = 'login')
def customer_profile(request):
    current_user = request.user
    profile = Customer.objects.get(user_id=current_user.id).first()
    return render(request, "profile.html", {"profile": profile})

@author_required(login_url = 'login')
def author_profile(request):
    current_user = request.user
    profile = Author.objects.filter(user_id=current_user.id).first()
    return render(request, "profile.html", {"profile": profile})


@institution_required(login_url = 'login')
def institution_profile(request):
    current_user = request.user
    profile = Institution.objects.filter(user_id=current_user.id).first()
    return render(request, "profile.html", {"profile": profile}) #change template


def profile(request):  # view profile
    current_user = request.user
    profile = Profile.objects.filter(user_id=current_user.id).first()  # get profile
    product = Product.objects.filter(author=current_user.author).all()  # get all projects
    return render(request, "profile.html", {"profile": profile,"image": product})
def update_profile(request,id):
    user = User.objects.get(id=id)
    profile = Profile.objects.get(user = user)
    form = UpdateProfileForm(instance=profile)
    if request.method == "POST":
            form = UpdateProfileForm(request.POST,request.FILES,instance=profile)
            if form.is_valid():  
                
                profile = form.save(commit=False)
                profile.save()
                return redirect('profile') 
            
    ctx = {"form":form}
    return render(request, 'update_profile.html', ctx)



#updating profiles
def update_customer_profile(request):
  if request.method == 'POST':
    # user_form = UpdateUserProfile(request.POST,request.FILES,instance=request.user)
    form = UpdateCustomerProfileForm(request.POST,request.FILES,instance=request.user)
    if form.is_valid():
    #   user_form.save()
      form.save()
      messages.success(request,'Your Profile account has been updated successfully')
      return redirect('profile')
  else:
    # user_form = UpdateUserProfile(instance=request.user)
    form = UpdateCustomerProfileForm(instance=request.user) 
  params = {
    # 'user_form':user_form,
    'form':form
  }
  return render(request,'edit_profile.html',params) #change template


def update_author_profile(request):
    if request.method == 'POST':
        # u_form = UpdateUserProfile(request.POST, request.FILES, instance=request.user)
        p_form = UpdateAuthorProfileForm(request.POST, instance=request.user)
        if p_form.is_valid():
            # u_form.save()
            p_form.save()
            messages.success(
                request, 'Your Profile account has been updated successfully')
            return redirect('profile')
    else:
        # u_form = UpdateUserProfile(instance=request.user)
        p_form = UpdateAuthorProfileForm(instance=request.user)
    context = {
        # 'u_form': u_form,
        'p_form': p_form
    }
    return render(request,'staff_profile.html',context) #change template

def update_institution_profile(request):
    if request.method == 'POST':
        # u_form = UpdateUserProfile(request.POST, request.FILES, instance=request.user)
        p_form = UpdateInstitutionProfileForm(request.POST, instance=request.user)
        if p_form.is_valid():
            # u_form.save()
            p_form.save()
            messages.success(
                request, 'Your Profile account has been updated successfully')
            return redirect('profile')
    else:
        # u_form = UpdateUserProfile(instance=request.user)
        p_form = UpdateInstitutionProfileForm(instance=request.user)
    context = {
        # 'u_form': u_form,
        'p_form': p_form
    }
    return render(request,'staff_profile.html',context) #change template

# @login_required
# def update_profile(request,id):
#     user = User.objects.get(id=id)
#     profile = Profile.objects.get(user_id = user)
#     form = UpdateProfileForm(instance=profile)
#     if request.method == "POST":
#             form = UpdateProfileForm(request.POST,request.FILES,instance=profile)
#             if form.is_valid():  
                
#                 profile = form.save(commit=False)
#                 profile.save()
#                 return redirect('profile') 
            
#     return render(request, 'edit_profile.html', {"form":form, 'profile':profile})
# REVIEW

def reviews(request):
    products = Product.objects.all()
   
    return render(request,"review.html",{'products':products})

#ordersystem
def index(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	if request.method == 'POST':
			form = ProductForm(request.POST, request.FILES)
			if form.is_valid():
					post = form.save(commit=False)
					post.user = request.user
					post.save()
					return HttpResponseRedirect(request.path_info)
	else:
			form = ProductForm()
	params = {
        'products':products,
				'form': form, 
        'cartItems':cartItems
        }
	return render(request, 'index.html', params)



def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	params = {
        'items':items, 
        'order':order, 
        'cartItems':cartItems
        }
	return render(request, 'cart.html', params)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	params = {
        'items':items, 
        'order':order, 
        'cartItems':cartItems
        }
	return render(request, 'checkout.html', params)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)


# like a book
@customer_required(login_url='login')
@author_required(login_url = 'login')
@institution_required(login_url = 'login')
def like_product(request, id):
    likes = Likes.objects.filter(product_id=id).first()
    # check if the user has already liked the image
    if Likes.objects.filter(product_id=id, user_id=request.user.id).exists():
        # unlike the image
        likes.delete()
        # reduce the number of likes by 1 for the image
        product = Product.objects.get(id=id)
        # check if the image like_count is equal to 0
        if product.like_count == 0:
            product.like_count = 0
            product.save()
        else:
            product.like_count -= 1
            product.save()
        return redirect('/')
    else:
        likes = Likes(product_id=id, user_id=request.user.id)
        likes.save()
        # increase the number of likes by 1 for the image
        product = Product.objects.get(id=id)
        product.like_count = product.like_count + 1
        product.save()
        return redirect('/')