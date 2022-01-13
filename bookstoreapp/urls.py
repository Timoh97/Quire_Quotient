from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

  


urlpatterns = [
  
    # path("uploading/", views.upload, name="upload"),
    # path("books/", views.books, name="books"),
    # path("upload/", views.upload, name="upload"),
    
    #Authentication
    # path('signup/', views.signup,name='signup'),
    # path('signup/customer/', views.customer_signup,name='customer_signup'),
    # path('signup/author/', views.author_signup,name='author_signup'),
    
    # REVIEWS
    path('reviews/', views.reviews,name="reviews"),
    
    #ordersystem
    path('', views.index, name="index"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
    path('login/',auth_views.LoginView.as_view(), name='login'),
    path('register/',views.register, name='register'),
    path('account/', include('django.contrib.auth.urls')),
    
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)