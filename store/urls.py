from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home, contact, detail, register, logout_user, add_item

from .forms import LoginForm

urlpatterns = [
    path ('', home, name='home'),
    path('contact/', contact, name='contact'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', logout_user, name= "logout"),
    path('add_item/', add_item, name='add_item'),
    path('detail/<int:pk>/', detail, name='detail'),
]
