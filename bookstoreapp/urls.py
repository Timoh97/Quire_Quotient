from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

  


urlpatterns = [
  
    path('signup/', views.signup,name='register'),
    path('signup/customer/', views.customer_signup,name='customer_signup'),
    path('signup/author/', views.author_signup,name='author_signup'),
    path('signup/institution/', views.institution_signup,name='institution_signup'),
    path('login/',views.login_view, name = 'login_view'),   
    path('logout/', views.logout, name='logout'),
    
    # REVIEWS
    path('reviews/', views.reviews,name="reviews"),
    path("profile/", views.profile, name="profile"),
    path("profile/update/<int:id>", views.update_profile, name="update_profile"),
    path('institution/profile/', views.institution_profile, name='institution_profile'),
    path('author/profile/', views.author_profile, name='author_profile'),
    path('customer/profile/', views.customer_profile, name='customer_profile'),
    path('update_author_profile/<int:id>',views.update_author_profile, name='update_author_profile'),
    path('update_customer_profile/<int:id>',views.update_customer_profile, name='update_customer_profile'),
    path('update_institution_profile/<int:id>',views.update_institution_profile, name='update_institution_profile'),
    #ordersystem
    path('', views.index, name="index"),
    
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
    path('login/',auth_views.LoginView.as_view(), name='login'),
    # path('register/',views.register, name='register'),
    path('account/', include('django.contrib.auth.urls')),
    
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)