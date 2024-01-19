from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

  


# urlpatterns = [
#   #all below urls are required
#     path('signup/', views.signup,name='register'),
#     path('signup/customer/', views.customer_signup,name='customer_signup'),
#     path('signup/author/', views.author_signup,name='author_signup'),
#     path('signup/institution/', views.institution_signup,name='institution_signup'),
#     path('login/',views.login_view, name = 'login_view'),   
#     path('logout/', views.logout, name='logout'),
#     path('reviews/', views.reviews,name="reviews"),
#     path('', views.index, name="index"),
# 	path('cart/', views.cart, name="cart"),
# 	path('checkout/', views.checkout, name="checkout"),
# 	path('update_item/', views.updateItem, name="update_item"),
# 	path('process_order/', views.processOrder, name="process_order"),
#     path('login/',auth_views.LoginView.as_view(), name='login'),
#     path('account/', include('django.contrib.auth.urls')),
    #all above urls are required
    # path("profile/", views.profile, name="profile"),
    # path("profile/update/", views.update_profile, name="update_profile"),
    # path('institution/profile/', views.institution_profile, name='institution_profile'),
    # path('author/profile/', views.author_profile, name='author_profile'),
    # path('customer/profile/', views.customer_profile, name='customer_profile'),
    # path('update_author_profile/<int:id>',views.update_author_profile, name='update_author_profile'),
    # path('update_customer_profile/<int:id>',views.update_customer_profile, name='update_customer_profile'),
    # path('update_institution_profile/<int:id>',views.update_institution_profile, name='update_institution_profile'),
     # path('register/',views.register, name='register'),
    #ordersystem
    

    
# ]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

urlpatterns = [
    path('', views.index, name="index"),
	  path('cart/', views.cart, name="cart"),
	  path('checkout/', views.checkout, name="checkout"),
	  path('update_item/', views.updateItem, name="update_item"),
	  path('process_order/', views.processOrder, name="process_order"),
    # path('login/',auth_views.LoginView.as_view(), name='login'),
    path('register/',views.register, name='register'),
    path('account/', include('django.contrib.auth.urls')),
    path('otp-verification/', views.otp_verification, name='otp_verification'),
    path('login/',views.login_view, name = 'login'),   
    path('logout/', views.logout_view, name='logout'),
    path('customer/<str:zen_name>/', views.customer_profile, name='customer_profile'),
    path('author/<str:zen_name>/', views.author_profile, name='author_profile'),
    path('reviews/', views.reviews, name='reviews'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    # path('customer_update/<str:zen_name>/', views.customer_update, name='customer_update'),
    # path('author_update/<str:zen_name>/', views.author_update, name='author_update'),
    
     # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('rate_product/<int:product_id>/', views.rate_product, name='rate_product'),

   
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)