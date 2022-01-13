from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import *
from .models import *

#AUTHENTICATION
from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from .forms import *
from. decorators import author_required

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

from .utils import cookieCart, cartData, guestOrder



# Create your views here.


# def upload(request):
# 	if request.method == "POST":
# 		form = BookForm(request.POST, request.FILES)
# 		if form.is_valid():
# 			form.save()
# 		return redirect("/")
# 	form = BookForm()
# 	books = Books.objects.all()
# 	return render(request=request, template_name="upload.html", context={'form':form, 'books':books})

# def books(request):
#     if request.method == "POST":
#         form = BookForm(request.POST, request.FILES)
#         if form.is_valid():
#             project = form.save(commit=False)
#             project.save()
#         return redirect('/')
#     else:
#         form = BookForm()
        
#     return render(request, 'books.html', {"form": form})


#AUTHENTICATION
# def signup(request):
#     '''View function to present users with account choices'''
#     title = 'Sign Up'
#     return render(request,'registration/signup.html',{'title': title})

# def customer_signup(request):
#     '''View function to sign up as a customer'''
#     if request.method == 'POST':
#         form = CustomerSignUp(request.POST)
#         import pdb; pdb.set_trace()
#         if form.is_valid():
#             user = form.save()
#             unhashed_password= form.cleaned_data.get('password1')
#             user = authenticate(username=user.username, password=unhashed_password)
#             login(request, user)
#             subject = 'Welcome to the BOOKSTORE!'
#             message = f'Hi {user.first_name},\nThe Bookstore would like to officially welcome you to our growing community. Browse the selection of books and find out all your reading tastes, see what you would like to purchase, and place your order.\nRemember to enjoy the app!\n\nKind Regards,\nThe Bookstore Management.'
#             email_from = settings.EMAIL_HOST_USER
#             recepient_list = [user.email,]
#             send_mail(subject,message,email_from,recepient_list)
#             messages.success(request, 'Account created successfully! Check your email for a welcome mail.')

#             return redirect('index')
#     else:
#         form= CustomerSignUp()

#     title = 'Customer Sign Up'
#     return render(request,'registration/signup_form.html',{'title': title,'form':form})

# def author_signup(request):
#     '''View function to sign up as an author'''
#     if request.method == 'POST':
#         form = AuthorSignUp(request.POST)
#         if form.is_valid():
#             user = form.save()
#             unhashed_password= form.cleaned_data.get('password1')
#             user = authenticate(username=user.username, password=unhashed_password)
#             login(request, user)
#             subject = 'Welcome to the BOOKSTORE!'
#             message = f'Hi {user.first_name},\nThe Bookstore would like to officially welcome you to our growing author community. Upload your books and have users browse the selection of books, view your uploaded book, and place their order.\nRemember to enjoy the app!\n\nKind Regards,\nThe Bookstore Management.'
#             email_from = settings.EMAIL_HOST_USER
#             recepient_list = [user.email,]
#             send_mail(subject,message,email_from,recepient_list)
#             messages.success(request, 'Account created successfully! Check your email for a welcome mail.')

#             return redirect('index')
#     else:
#         form= AuthorSignUp()

#     title = 'Author Sign Up'
#     return render(request,'registration/signup_form.html',{'title': title,'form':form})


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

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            messages.success(request, f'Your account has been created! You are now able to log in {username}.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form}) 

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