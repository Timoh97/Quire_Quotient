from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404,HttpResponseRedirect, JsonResponse
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import User
import json
from django.contrib.auth.decorators import login_required
from. decorators import *
import datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder
from .forms import *
from datetime import datetime, timedelta
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.utils import timezone
from . safaricom_credentials import MpesaAccessToken, LipanaMpesaPpassword
from bookstore.settings import *
import requests
from requests.auth import HTTPBasicAuth
from django_daraja.mpesa.core import MpesaClient

cl = MpesaClient()
# Create your views here.
def generate_otp():
    return get_random_string(length=6, allowed_chars='0123456789')

def send_otp_email(email, otp):
    subject = 'One-Time Password'
    message = f'Your OTP is: {otp}. It will expire in one minute.'
    from_email=EMAIL_SENDER  
    send_mail(subject, message, from_email, [email])
    
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
        'cartItems':cartItems,
        # 'customer':customer,
        # 'author':author
        }
	return render(request, 'index.html', params)

def customer_profile(request, zen_name):
    customer_profile = get_object_or_404(Customer, user__zen_name=zen_name)

    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=customer_profile)
        if form.is_valid():
            form.save()
            return redirect('customer_profile')  # Redirect to customer profile page

    else:
        form = CustomerProfileForm(instance=customer_profile)

    context = {
        'form': form,
    }
    return render(request,'customer_profile.html',context)

def author_profile(request, zen_name):
    author_profile = get_object_or_404(Author, user__zen_name=zen_name)
    

    if request.method == 'POST':
        form = AuthorProfileForm(request.POST, instance=author_profile)
        if form.is_valid():
            form.save()
            return redirect('author_profile')  # Redirect to author profile page

    else:
        form = AuthorProfileForm(instance=author_profile)

    context = {
        'form': form,
    }
    return render(request,'author_profile.html',context)

# # @login_required
# def author_update(request, zen_name):
#     user = get_object_or_404(User, username=zen_name, is_author=True)

#     if request.method == 'POST':
#         a_form = AuthorProfileForm(request.POST, request.FILES, instance=user)
#         if a_form.is_valid():
#             a_form.save()
#             return JsonResponse({'status': 'success'})
#         else:
#             return JsonResponse({'status': 'error', 'errors': a_form.errors})
#     else:
#         a_form = AuthorProfileForm(instance=user)

#     return render(request, 'author_profile.html', {'a_form': a_form})


def rate_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.product = product
            rating.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = RatingForm()

    return render(request, 'rate_product.html', {'form': form, 'product': product})


def reviews(request):
    
    
    return render(request,'reviews.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        user_type = request.POST.get('user_type') 
        if form.is_valid():
            user = form.save()
            otp = generate_otp()

            if user_type == 'Author':
                author = getattr(user, 'author', None)
                if author:
                    author.otp = otp
                    author.otp_expires_at = timezone.now() + timedelta(minutes=1)
                    author.save()
            elif user_type == 'Customer':
                customer = getattr(user, 'customer', None)
                if customer:
                    customer.otp = otp
                    customer.otp_expires_at = timezone.now() + timedelta(minutes=3)
                    customer.save()

            # Send OTP to the user's email
            send_otp_email(user.email, f'Your account has been created!\nYour One-time password is: {otp}.')

            # Authenticate the user
            authenticated_user = authenticate(request, email=user.email, password=form.cleaned_data['password1'])
            if authenticated_user and isinstance(authenticated_user, User):
                login(request, authenticated_user)

            messages.success(request, f'Your account has been created! Check your email for the OTP.')
            return redirect('otp_verification')  # Redirect to OTP verification page
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})




def otp_verification(request):
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']

            # Check if the user is an Author or Customer
            if hasattr(request.user, 'customer'):
                user_profile = request.user.customer
            elif hasattr(request.user, 'author'):
                user_profile = request.user.author
            else:
                # Handle the case where the user doesn't have a valid profile
                messages.error(request, 'Invalid user profile. Please contact support.')
                return redirect('otp_verification')

            # Check the OTP and expiration time
            if (
                user_profile.otp == entered_otp
                and user_profile.otp_expires_at is not None
                and user_profile.otp_expires_at > timezone.now()
            ):
                # Clear OTP and expiration time after successful verification
                user_profile.otp = None
                user_profile.otp_expires_at = None
                user_profile.save()

                messages.success(request, 'OTP verification successful. You are now logged in.')
                return redirect('login')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
    else:
        form = OTPVerificationForm()

    return render(request, 'registration/otp_verification.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            # Authenticate the user
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)

               
                if hasattr(user, 'customer'):
                    messages.info(request, f"You are now logged in as a Customer using {email}.")
                elif hasattr(user, 'author'):
                    messages.info(request, f"You are now logged in as an Author using {email}.")
                else:
                    messages.error(request, 'Invalid user profile. Please contact support.')

                return redirect('index')
            else:
                messages.error(request, 'Invalid email or password. Please try again.')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

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

@login_required
def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']


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

def book_detail(request, book_id):
    book = get_object_or_404(Product, id=book_id)
    comments = Comment.objects.filter(book=book)
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.book = book
            comment.save()
            return redirect('book_detail', book_id=book.id)

    return render(request, 'book_detail.html', {'book': book, 'comments': comments, 'form': form})

def getAccessToken(request):
    consumer_key= c2b_consumer_key #input your consumer key from the sandbox  
    consumer_secret  = c2b_consumer_secret #input your consumer secret from the sandbox
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

    mpesa_access_token = r.json()
    validated_mpesa_access_token = mpesa_access_token['access_token']
    
    return HttpResponse(validated_mpesa_access_token)

def stk_push_success(request, ph_number, totalAmount):
    # Access the phone_number value from the submitted form data
    access_token = MpesaAccessToken.validated_mpesa_access_token
    stk_push_callback_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    print(access_token)
    headers = {"Authorization": "Bearer %s" % access_token}

    phone_number = ph_number
    amount = totalAmount
    request_load = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": 254714919899,  # replace with your phone number to get stk push
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": phone_number,  # replace with your phone number to get stk push
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "hacker",
        "TransactionDesc": "Testing stk push"
    }

    # Assuming MpesaClient is instantiated with the necessary configurations
    cl = MpesaClient()

    # Adjust the method signature based on MpesaClient implementation
    response = cl.stk_push(phone_number, amount, stk_push_callback_url ,headers=headers, json=request_load)
    return HttpResponse(response)

def payment(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        amount = request.POST.get('amount')

        ph_number = None
        totalAmount = int(float(amount))

        if phone_number[0] == '0':
            ph_number = '254' + phone_number[1:]
        elif phone_number[0:2] == '254':
            ph_number = phone_number
        else:
            return redirect(request.get_full_path())

        stk_push_success(request, ph_number, totalAmount)
    
        tel_nummer= phone_number
        money=amount

        return render(request, 'success.html',{'phone_number': tel_nummer, 'amount': money})




    return render(request,'checkout.html')
