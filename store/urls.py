from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home, contact, detail, register

from .forms import LoginForm

urlpatterns = [
    path ('', home, name='home'),
    path('contact/', contact, name='contact'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html', authentication_form=LoginForm)),
    path('detail/<int:pk>/', detail, name='detail')
]
