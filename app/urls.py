from django.urls import path, include

from django.contrib.auth import views as auth_views #To import the views from the django authentication module.

from . import views
urlpatterns = [
    
    path('', views.IndexPage, name = 'home'),
    path('login', views.LoginPage, name = 'login'),
    path('register', views.RegisterPage, name='register'),
    path('products', views.ProductsPage, name="products"),
    path('customer/<str:pk>', views.CustomerPage, name="customer"),
    path('create_order', views.OrderPage, name="create_order"),
    path('update_order/<str:pk>', views.UpdatePage, name="update_order"),
    path('delete_order/<str:pk>', views.DeletePage, name="delete_order"),
    path('place_order/<str:pk>', views.PlaceOrder, name = "place_order"),
    path('logout', views.LogoutUser, name="logout_user"),
    path('user', views.UserPage, name="user_page"),
    path('profile', views.ProfilePage, name="profile"),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = 'password_reset.html'), name="reset_password"),
    path("password_reset_sent/", auth_views.PasswordResetDoneView.as_view(template_name = 'password_reset_sent.html'), name = "password_reset_done"),
    path("reset/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view(template_name = 'password_reset_form.html'), name = "password_reset_confirm"),
    path("password_reset_complete/", auth_views.PasswordResetCompleteView.as_view(template_name = 'password_reset_done.html'), name = "password_reset_complete"),

]