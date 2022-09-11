from django.urls import path

from ecommerce.users.views import UserRegister, login_page

urlpatterns = [
    path('register/', UserRegister.as_view(), name='register'),
    path('login/', login_page,name='login'),

]
