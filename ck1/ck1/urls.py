"""ck1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views 
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from app.forms import MychangePasswordForm
from .import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('master/',views.Master,name='master'),
    path('',views.Index,name='index'),
    path('signup',views.signup,name='signup'),
    path('accounts/',include('django.contrib.auth.urls')),
    path('about/',views.About_Page,name='about_page'),
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
    path('contact/',views.Contact_Page,name='contact_page'),
    path('search/',views.Search,name='search'),
    path('checkout/',views.CheckOut,name ='checkout'),
    path('order/',views.Your_Order,name ='order'),
    path('product/',views.Product_Page ,name = 'product'),
    path('product/<str:id>',views.Product_Detail,name = 'product_detail'),
    path('htmlfile/',views.HtmlFile,name ='htmlfile'),
    path('placeorder/',views.PLACE_ORDER,name ='place_order'),
    path('my-dashboard/',views.my_dashboard,name= 'my_dashboard'),
    path('success',views.success,name="success"),
    path('wishlist/',views.wishlist,name="wishlist"),
    path('my_order',views.My_Order,name="my_order"),
    path('add-address/', views.AddressView.as_view(), name="add-address"),
    path('updateprofile/', views.Update_Profile, name="updateprofile"),
    path('upd/', views.UPD, name="upd"),
    path('Review_rate/<int:product_id>', views.Review_rate, name="Review_rate"),
    

    # Forget Password
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),


    # Change password
    path('change-password/',PasswordChangeView.as_view(template_name="user/change-password.html", form_class=MychangePasswordForm), name='change-password'),
    path('password-change-done/', PasswordChangeDoneView.as_view(template_name="user/password-change-done.html"), name="password_change_done")
    

] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
