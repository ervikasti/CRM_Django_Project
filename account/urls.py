from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('product/', views.product, name="product"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('create_customer/', views.createCustomer, name="create_customer"),

    path('customer/<int:pk>', views.customer, name="customer"),
    path('create_order/<int:pk>/', views.createOrder, name="create_order"),
    path('update_order/<int:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<int:pk>/', views.deleteOrder, name="delete_order"),
    path('register/', views.registerPage, name="register"),
    
]

