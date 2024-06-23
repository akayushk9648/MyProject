from django.urls import path
from . import views

urlpatterns = [
    path('index/',views.index),
    path('',views.index),
    path('indexcart/',views.indexcart),
    path('contact/',views.contact),
    path('about/',views.aboutus),
    path('signin/',views.signin),
    path('signup/',views.signup),
    path('product/',views.product),
    path('signout/',views.signout),
    path('myprofile/',views.myprofile),
    path('mycart/',views.mycart),
    path('cartitem/',views.cartitem),
    path('registered/',views.already),
    path('mprofile/',views.mprofile),
    path('orderitem/',views.orders),
    path('thank/',views.thank),
    path('orders/',views.orders),
    path('successreg/',views.successreg),
    path('profupdate/',views.profupdate),
    
]
