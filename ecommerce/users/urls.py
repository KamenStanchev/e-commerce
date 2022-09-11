from django.urls import path

from ecommerce.users.views import UserRegister, login_page, LogoutView

urlpatterns = [
    path('register/', UserRegister.as_view(), name='register'),
    path('login/', login_page,name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

]
